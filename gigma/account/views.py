from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Discipline, ProfileDisciplines
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from gigma.settings import MEDIA_URL
from django.urls import is_valid_path
from urllib.parse import urlparse

@login_required
def dashboard(request):
	profile = Profile.objects.get(user_id=request.user)
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request, "account/dashboard.html",{'section':'dashboard','profile':profile, 'media_url': MEDIA_URL, 'my_profile':my_profile})

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			#create user obj but don't save until after password validation
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data['password'])
			new_user.save()
			#Create user profile attached to this account
			Profile.objects.create(user=new_user)
			return render(request,'account/register_done.html',{'new_user': new_user})
	else:
		form = UserRegistrationForm()
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request,'account/register.html',{'form':form, 'my_profile':my_profile})

def login_view(request):
	next_url = request.GET.get('next', '/')

	if request.method == 'POST':
		user = authenticate(request, username=request.POST["username"],
                            password=request.POST["password"])
		if user:
			login(request, user)
			messages.success(request, 'Logged in successfully')
            # Ensure next_url is safe or default to home page
			next_url = request.POST.get('next', next_url)
			parsed_url = urlparse(next_url)
			if not parsed_url.netloc and is_valid_path(next_url):
				return redirect(next_url)
			return redirect('/')

		else:
			messages.error(request, 'Login Failed')
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request, 'registration/login.html',{'my_profile':my_profile, 'next': next_url})

def logout_view(request):
	logout(request)
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request, 'registration/logged_out.html',{'my_profile':my_profile})

@login_required
def edit(request):
	if request.method == 'POST':
		print(request.FILES)
		user_form = UserEditForm(instance=request.user,data=request.POST,prefix="user")
		profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES,prefix="profile")
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated successfully')
		else:
			messages.error(request, 'Error updating your profile')
	else:
		try:
			Profile.objects.get(user_id=request.user)
		except:
			Profile.objects.create(user=request.user)
		user_form = UserEditForm(instance=request.user,prefix="user")
		profile_form = ProfileEditForm(instance=request.user.profile,prefix="profile")
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form, 'my_profile':my_profile})

@login_required
def edit_disciplines(request):
	if request.method == 'POST':
		discipline_id = request.POST.get('new_discipline')
		ProfileDisciplines.objects.create(
			profile = Profile.objects.get(user_id=request.user),
			discipline = Discipline.objects.get(id=discipline_id),
			skill_level = 3,
			profile_discipline_order = 1
		)

	profile = Profile.objects.get(user_id=request.user)
	disciplines = Discipline.objects.all()
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request,'account/edit_disciplines.html',{'profile':profile,'disciplines':disciplines, 'my_profile':my_profile})


def profile_search(request):
	profiles = Profile.objects.all().exclude(user_id=1)
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request, 'account/profile_search.html',{'section':'dashboard','profiles':profiles, 'my_profile':my_profile})

def profile_details(request, id=None):
	profile = Profile.objects.get(id=id)
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request, 'account/profile_details.html',{'section':'dashboard','profile':profile, 'my_profile':my_profile})

def discipline_list(request):
	disciplines = Discipline.objects.filter(parent_discipline__isnull=True)
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request, 'account/discipline_list.html',{'section':'discipline_list','disciplines':disciplines, 'my_profile':my_profile})