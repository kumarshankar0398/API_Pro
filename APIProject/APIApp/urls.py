from django.urls import path
from .views import Record, Login, Logout, ResetPassword, ResetYourPassword

urlpatterns = [
    path('', Record.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('reset/', ResetPassword.as_view(), name="reset"),
    path('resetpwd/', ResetYourPassword.as_view(), name="resetpwd"),
]






