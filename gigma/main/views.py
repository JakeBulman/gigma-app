from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import Profile
from gigma.settings import MEDIA_URL

# Create your views here.
def landing_page(request):
    my_profile = None
    if request.user.is_authenticated:
        try:
            my_profile = Profile.objects.get(user_id=request.user)      
        except:
            my_profile = Profile.objects.create(user=request.user)    
           		
    return render(request, "main/landing_page.html",{'section':'landing_page', 'media_url': MEDIA_URL, 'my_profile':my_profile})