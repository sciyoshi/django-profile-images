import Image

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from django.conf import settings
from django.db import models

class ProfileImageManager(models.Manager):
    def save_from_info(self, user, info):
        profile, created = self.get_or_create(user=user)
        image = Image.open(StringIO.StringIO(info['content']))
        profile.image = '%s%s.%s' % (settings.PROFILE_IMAGE_UPLOAD_DIR, user.id, image.format.lower())
        image.save(profile.get_image_filename())
        profile.save()
        return profile
