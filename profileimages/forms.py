import Image

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from django import newforms as forms
from django.conf import settings

from models import ProfileImage

class ProfileImageForm(forms.Form):
    """
    Profile image upload form.
    """

    image = forms.Field(widget=forms.FileInput())

    def clean_image(self):
        if 'image' in self.cleaned_data:
            image = self.cleaned_data['image']
            if len(image['content']) > settings.PROFILE_IMAGE_MAX_SIZE * 1024:
                raise forms.ValidationError('The image you are trying to upload is larger than %d Kb.' % settings.PROFILE_IMAGE_MAX_SIZE)
            try:
                data = Image.open(StringIO.StringIO(image['content']))
                data.verify()
            except:
                raise forms.ValidationError('The file you are uploading does not seem to be an image.')
            return image

    def save(self, user):
        profile, created = ProfileImage.objects.get_or_create(user=user)
        profile.save_image_file(self.cleaned_data['image']['filename'], self.cleaned_data['image']['content'])
        return profile
