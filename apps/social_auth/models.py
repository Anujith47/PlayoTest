from django.db import models
from django.contrib.auth.models import AbstractUser as DjangoUser


class SocialUser(DjangoUser):
    """
    The Social User inherited from Django User
    """
    nick_name = models.CharField(max_length=24, null=True, blank=True)

    @property
    def profile_name(self):
        return str(self)

    def __str__(self):
        if self.nick_name:
        	return "{} {} ({})".format(
        		self.first_name, self.last_name, self.nick_name)
        else:
            return "{} {}".format(
        		self.first_name, self.last_name)
