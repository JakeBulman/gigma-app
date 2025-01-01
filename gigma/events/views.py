from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import NewEventForm
from account.models import Profile
from gigma.settings import MEDIA_URL

# Create your views here.
@login_required
def dashboard(request):
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	if my_profile.account_type == 'ORG':
		return redirect('organiser_events')
	elif my_profile.account_type == 'ART':
		return redirect('artist_events')
	else:
		return redirect('event_search')
	
@login_required
def organiser_events(request,event_id=None):
	events=None
	if Event.objects.filter(event_organiser=request.user).exists():
		events = Event.objects.filter(event_organiser=request.user)
	
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)

	selected_event = None
	if event_id and Event.objects.filter(pk=event_id,event_organiser=request.user).exists():
		selected_event = Event.objects.get(pk=event_id,event_organiser=request.user)

	return render(request, 'events/organiser_events.html',{'section':'dashboard','events':events, 'media_url': MEDIA_URL, 'my_profile':my_profile, 'selected_event':selected_event})

@login_required
def new_event(request):
	events=None
	if Event.objects.filter(event_organiser=request.user).exists():
		events = Event.objects.filter(event_organiser=request.user)
	
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	form = NewEventForm()
	return render(request, 'events/new_event.html',{'form':form,'section':'dashboard','events':events, 'media_url': MEDIA_URL, 'my_profile':my_profile})

@login_required
def new_event_created(request):
	if request.method == 'POST':
		event_form = NewEventForm(request.POST)
		if event_form.is_valid():
			#create user obj but don't save until after password validation
			new_user = event_form.save(commit=False)
			new_user.set_password(event_form.cleaned_data['password'])
			new_user.save()
			#Create user profile attached to this account
			Profile.objects.create(user=new_user)
			return render(request,'account/register_done.html',{'new_user': new_user})

	#TODO: Need to redirect to newly created event
	return render(request,'account/register.html',{'event_form':event_form})

@login_required
def artist_events(request):
	events=None
	if Event.objects.filter(event_organiser=request.user).exists():
		events = Event.objects.filter(event_organiser=request.user)
	
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request, 'events/artist_events.html',{'section':'dashboard','events':events, 'media_url': MEDIA_URL, 'my_profile':my_profile})

def event_search(request):
	events = Event.objects.all()
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request, 'events/event_search.html',{'section':'dashboard','events':events, 'my_profile':my_profile})

def event_details(request, id=None):
	event = Event.objects.get(id=id)
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request, 'events/event_details.html',{'section':'dashboard','event':event, 'my_profile':my_profile})

