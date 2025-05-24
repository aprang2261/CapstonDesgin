from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import render, redirect

def main(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return redirect("jwt_login")

    try:
        AccessToken(token)  # 유효한 토큰인지 검증
    except Exception:
        return redirect("jwt_login")  # 만료되었거나 변조된 토큰

    return render(request, "main.html")