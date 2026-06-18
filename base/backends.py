from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # We use `username` here because the AuthenticationForm passes the email in the `username` kwarg
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # If multiple users have the same email, we'll just take the first one to be safe
            user = User.objects.filter(email=username).order_by('id').first()
            
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
