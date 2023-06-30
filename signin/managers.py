from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where steamid is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, steamid, password, **extra_fields):
        """
        Create and save a User with the given steamid and password.
        """
        if not steamid:
            raise ValueError(_('The steamid must be set'))
        user = self.model(steamid=steamid, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, steamid, password, **extra_fields):
        """
        Create and save a SuperUser with the given steamid and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(steamid, password, **extra_fields)
