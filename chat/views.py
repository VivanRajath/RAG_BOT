import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import UploadedFile, ChatHistory
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()

User = get_user_model()

# Hugging Face backend URLs
HF_PIPELINE_UPLOAD_URL = os.getenv("HF_PIPELINE_UPLOAD_URL", "https://vivanrajath-test2.hf.space/upload-pdf")
HF_PIPELINE_ASK_URL = os.getenv("HF_PIPELINE_ASK_URL", "https://vivanrajath-test2.hf.space/ask")

# -------------------- AUTH --------------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("home")
    return render(request, "signup.html")


# -------------------- HOME / UPLOAD --------------------

def home(request):
    uploaded_file_url = None
    if request.method == "POST" and request.FILES.get("uploaded_file"):
        uploaded_file = request.FILES["uploaded_file"]
        new_file = UploadedFile.objects.create(
            owner=request.user if request.user.is_authenticated else None,
            file=uploaded_file
        )
        uploaded_file_url = new_file.file.url

        # Upload PDF to HF backend safely
        try:
            with open(new_file.file.path, "rb") as f:
                files = {"file": f}
                resp = requests.post(HF_PIPELINE_UPLOAD_URL, files=files, timeout=30)
                if resp.status_code != 200:
                    print("HF upload failed:", resp.text)
        except requests.exceptions.RequestException as e:
            print("Error uploading to HF backend:", e)

        return redirect("chat", file_id=new_file.id)

    # Show files only for the logged-in user
    if request.user.is_authenticated:
        all_files = UploadedFile.objects.filter(owner=request.user).order_by("-uploaded_at")
    else:
        all_files = []  # Anonymous users see nothing

    return render(request, "home.html", {"uploaded_file_url": uploaded_file_url, "all_files": all_files})


# -------------------- CHAT --------------------

def chat_view(request, file_id):
    # Make sure only the owner can access their file
    if request.user.is_authenticated:
        current_file = get_object_or_404(UploadedFile, id=file_id, owner=request.user)
    else:
        return redirect("login")  # Force login for chat access

    if request.method == "POST":
        query = request.POST.get("query")
        answer = "I couldn't find that in the document."

        # Send query to HF backend safely
        try:
            with open(current_file.file.path, "rb") as f:
                files = {"file": f}
                data = {"query": query}
                resp = requests.post(HF_PIPELINE_ASK_URL, files=files, data=data, timeout=30)
                if resp.status_code == 200:
                    answer = resp.json().get("answer", answer)
                else:
                    print("HF ask failed:", resp.text)
        except requests.exceptions.RequestException as e:
            print("Error sending to HF backend:", e)

        # Save chat history only for logged-in user
        ChatHistory.objects.create(user=request.user, file=current_file, query=query, answer=answer)

        return JsonResponse({"answer": answer})

    # Show chat history only for the logged-in user
    user_history = ChatHistory.objects.filter(user=request.user, file=current_file)

    return render(request, "chat.html", {
        "current_file": current_file,
        "other_files": UploadedFile.objects.filter(owner=request.user).exclude(id=current_file.id),
        "chat_history": user_history
    })
