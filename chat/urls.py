from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),


    # Home / Upload
    path("", views.home, name="home"),

    # Chat per file
    path("file/<int:file_id>/", views.chat_view, name="chat"),
    path('accounts/login/', views.login_view),

]
