
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UploadedFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to="uploads/")
    title = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.file.name

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    query = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class IndexStore(models.Model):
    """
    Store FAISS index metadata.
    - 'global' for knowledge base
    - 'temp' for per-user/per-file session
    """
    name = models.CharField(max_length=100)  # 'global' or 'temp'
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file_obj = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, null=True, blank=True)
    faiss_data = models.BinaryField(null=True, blank=True)  # Store serialized FAISS index
    docs_data = models.BinaryField(null=True, blank=True)   # Store serialized doc chunks
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("owner", "name", "file_obj"),)

    def __str__(self):
        return f"{self.name} - {self.owner or 'global'} - {self.file_obj or 'NA'}"
