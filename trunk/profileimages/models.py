from PIL import Image

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.admin import site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import signals
from django.dispatch import dispatcher

from managers import ProfileImageManager

class ProfileImage(models.Model):
    user = models.ForeignKey(User, unique=True)
    image = models.ImageField(upload_to=settings.PROFILE_IMAGE_UPLOAD_DIR, null=True)

    objects = ProfileImageManager()

    def __str__(self):
        return '%s\'s Profile Image' % self.user

    def _save_FIELD_file(self, field, filename, raw_contents, save):
        image = Image.open(StringIO.StringIO(raw_contents))
        self.image = '%s%s.%s' % (settings.PROFILE_IMAGE_UPLOAD_DIR, self.user.id, image.format.lower())
        image.save(self.get_image_filename())
        if save:
            self.save()

def create_default_profile_image(sender, instance, **kwargs):
    profile, created = ProfileImage.objects.get_or_create(user=instance)
    if created:
        profile.image = settings.PROFILE_IMAGE_DEFAULT
        profile.save()

dispatcher.connect(create_default_profile_image, sender=User, signal=signals.post_save)

site.register(ProfileImage)
