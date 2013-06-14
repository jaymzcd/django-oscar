from django.db import models
from django.utils import timezone

from django.contrib.auth import models as auth_models

from oscar.core import compat


class Profile(models.Model):
    """
    Dummy profile model used for testing
    """
    user = models.OneToOneField(compat.AUTH_USER_MODEL, related_name="profile")
    MALE, FEMALE = 'M', 'F'
    choices = (
        (MALE, 'Male'),
        (FEMALE, 'Female'))
    gender = models.CharField(max_length=1, choices=choices,
                              verbose_name='Gender')
    age = models.PositiveIntegerField(verbose_name='Age')


# A simple extension of the core User model
class ExtendedUserModel(auth_models.AbstractUser):
    twitter_username = models.CharField(max_length=255, unique=True)


class CustomUserManager(auth_models.BaseUserManager):

    def create_user(self, email, password=None):
        now = timezone.now()
        email = auth_models.BaseUserManager.normalize_email(email)
        user = self.model(email=email, last_login=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        return self.create_user(email, password)


# A user model which doesn't extend AbstractUser
class CustomUserModel(auth_models.AbstractBaseUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    twitter_username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return self.name

    get_short_name = get_full_name
