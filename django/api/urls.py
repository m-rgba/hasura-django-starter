from django.urls import path, include
from django.conf.urls import url, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .auth import HasuraTokenObtainPair, RegisterUser, ChangePassword
from . import logic

urlpatterns = (
    path('token/', HasuraTokenObtainPair.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/register/', RegisterUser.as_view(), name='register_user'),
    path('user/change_password/', ChangePassword.as_view(), name='change_password'),
    url('user/', include('django_rest_passwordreset.urls', namespace='password_reset')), 
            # + /reset_password/ 
            # + /rest_password_confirm/ 
            # + /reset_password/validate_token/
    # >>> Logic Samples
    path('logic/new_registration_email/', logic.new_registration_email, name='email_registration'),
    path('logic/reset_password_email/', logic.reset_password_email, name='email_reset_password'),
    path('logic/hotdog/', logic.is_hotdog, name='is_hotdog'),
)