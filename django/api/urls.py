from django.urls import path, include
from django.conf.urls import url, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .auth import HasuraTokenObtainPair, ValidateTokenRefreshView, RegisterUser, ChangePassword
from . import sample_emails
from . import sample_logic

urlpatterns = (
    path('logic/healthcheck/', sample_logic.healthcheck, name='healthcheck'),
    path('login/', HasuraTokenObtainPair.as_view(), name='token_obtain_pair'),
    path('token/refresh/', ValidateTokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', RegisterUser.as_view(), name='register_user'),
    path('user/change_password/', ChangePassword.as_view(), name='change_password'),
    url('reset_password/', include('django_rest_passwordreset.urls', namespace='password_reset')), 
            # + /reset_password/ 
            # + /reset_password/confirm/ 
            # + /reset_password/validate_token/
    # >>> Logic Samples
    path('emails/new_registration_email/', sample_emails.new_registration_email, name='email_registration'),
    path('emails/reset_password_email/', sample_emails.reset_password_email, name='email_reset_password'),
    path('logic/action_sample/', sample_logic.action_sample, name='logic_action'),
)