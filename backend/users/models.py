from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email or password is None:
            raise ValueError('Required.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email or password is None:
            raise ValueError('Required.')

        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def has_perm(*args, **kwargs):
        return True

    def has_module_perms(*args, **kwargs):
        return True

    def __str__(self):
        return self.email
