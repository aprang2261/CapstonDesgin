from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.http import require_http_methods
import requests

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer


API_URL = settings.API_BASE_URL  # settings.py에 반드시 정의되어 있어야 함


def extract_error_message(data):
    """에러 메시지를 유연하게 추출하는 함수"""
    for key, value in data.items():
        if isinstance(value, list) and value:
            return value[0]
        elif isinstance(value, str):
            return value
    return "알 수 없는 오류가 발생했습니다."


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@require_http_methods(["GET", "POST"])
def jwt_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            return render(request, "accounts/jwt-register.html", {
                "error": "비밀번호가 일치하지 않습니다."
            })

        response = requests.post(f"{API_URL}/api/accounts/register/", json={
            "username": username,
            "email": email,
            "password": password,
            "password2": password2
        })

        if response.status_code == 201:
            return redirect("jwt_login")

        try:
            data = response.json()
            error_msg = extract_error_message(data)
        except Exception:
            error_msg = "회원가입 중 오류가 발생했습니다."

        return render(request, "accounts/jwt-register.html", {
            "error": error_msg
        })

    return render(request, "accounts/jwt-register.html")


@require_http_methods(["GET", "POST"])
def jwt_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        response = requests.post(f"{API_URL}/api/accounts/login/", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access")
            refresh_token = data.get("refresh")

            res = redirect("main")
            res.set_cookie("access_token", access_token, httponly=True, secure=True, samesite='Lax')
            res.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite='Lax')
            return res

        return render(request, "accounts/jwt-login.html", {
            "error": "아이디 또는 비밀번호가 올바르지 않습니다."
        })

    return render(request, "accounts/jwt-login.html")


@require_http_methods(["GET", "POST"])
def jwt_logout(request):
    response = redirect("jwt_login")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response