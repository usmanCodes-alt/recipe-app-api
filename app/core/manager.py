from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create, save and return the new user
        """
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)     # creates hash of the password
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates a super user
        """
        user = self.create_user(email=email, password=password)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user
