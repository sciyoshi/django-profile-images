import os

from django.db.models import get_model
from django.template import Library, Node, TemplateSyntaxError, resolve_variable
from django.conf import settings

import Image

from profileimages.models import ProfileImage

register = Library()

class ProfileImageNode(Node):
    def __init__(self, user, size='100x100', square=False):
        self.user = user
        self.size = size
        self.square = square

    def render(self, context):
        user = resolve_variable(self.user, context)
        image = ProfileImage.objects.get(user=user)
        filename = image.get_image_filename()
        try:
            mtime1 = os.stat(filename).st_mtime
        except:
            return
        x, y = [int(x) for x in self.size.split('x')]
        basename, format = image.image.rsplit('.', 1)
        miniature = basename + '_' + self.size + '.' + format
        miniature_filename = os.path.join(settings.MEDIA_ROOT, miniature)
        miniature_url = os.path.join(settings.MEDIA_URL, miniature)
        try:
            mtime2 = os.stat(miniature_filename).st_mtime
        except:
            mtime2 = 0
        if mtime2 < mtime1:
            image = Image.open(filename)
            image.thumbnail([x, y], Image.ANTIALIAS)
            image.save(miniature_filename, image.format)
        if self.square:
            return """<img src="%s" alt="%s's Profile Image" />""" % (miniature_url, user)
        return """<img src="%s" alt="%s's Profile Image" />""" % (miniature_url, user)

@register.tag
def profile_image(parser, token):
    bits = token.contents.split()
    if len(bits) not in (2, 3, 4):
        raise TemplateSyntaxError
    if len(bits) == 2:
        return ProfileImageNode(bits[1])
    if len(bits) == 3:
        return ProfileImageNode(bits[1], bits[2])
    if len(bits) == 4:
        if bits[3] != 'square':
            raise TemplateSyntaxError
        return ProfileImageNode(bits[1], bits[2], True)
