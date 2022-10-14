from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    """
        User Account Manger
    """

    def create_user(self, mobile: str, password=None):
        """
            Creates and Saves a User with the Given Username, Mobile Number and Password.
        """
        if not mobile:
            raise ValueError("Users Must Have an Valid Mobile!")

        user = self.model(mobile=mobile)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  mobile: str, phone: str, password=None):
        """
            Creates and Saves a User with the Given Mobile Number and Password.
        """
        user = self.create_user(mobile, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
        User Account Model
    """
    mobile = models.CharField(max_length=11, unique=True)
    credit = models.IntegerField(default=7)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mobile


class UserRequest(models.Model):
    """
        User Request Model
    """
    user_ip = models.CharField(max_length=128, unique=True)
    credit = models.IntegerField(default=2)
