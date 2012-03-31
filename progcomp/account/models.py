from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test


class Profile(models.Model):

    user   = models.OneToOneField(User, unique=True)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    grad   = models.DateField()
    resume = models.FileField(upload_to='resumes/%Y-%m-%d', blank=True)

    def __str__(self):
        return str(self.user)


is_registered = user_passes_test(lambda u:
        u.is_authenticated() and
        Profile.objects.filter(user=u.pk).count() > 0)
