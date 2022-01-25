from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class TeacherManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)


class StudentManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()
    teachers = TeacherManger()
    students = StudentManger()

    USERNAME_FIELD = 'email'

    @property
    def is_teacher(self):
        return self.is_staff
