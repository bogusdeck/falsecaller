from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number must be set")
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(blank=True, null=True)
    token = models.CharField(max_length=100)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.phone_number


class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class SpamReport(models.Model):
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Spam report for {self.phone_number} by {self.reported_by}"
