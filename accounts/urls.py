from django.urls import path
from .views import RegisterView, jwt_register, jwt_login, jwt_logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # HTML 페이지용
    path('jwt-register/', jwt_register, name='jwt_register'),
    path('jwt-login/', jwt_login, name='jwt_login'),
    path('jwt-logout/', jwt_logout, name='jwt_logout'),
]