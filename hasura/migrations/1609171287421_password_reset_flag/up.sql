ALTER TABLE public.django_rest_passwordreset_resetpasswordtoken
  ADD COLUMN "reset_sent" BOOLEAN DEFAULT FALSE;