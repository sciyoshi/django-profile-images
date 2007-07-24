from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

from forms import ProfileImageForm
from models import ProfileImage

@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data.update(request.FILES)
        form = ProfileImageForm(data)
        if form.is_valid():
            ProfileImage.objects.save_from_info(request.user, form.cleaned_data['image'])
            return HttpResponseRedirect('/')
    else:
        form = ProfileImageForm()

    return direct_to_template(request, 'profileimages/image_upload.html', {'image_upload_form': form})
