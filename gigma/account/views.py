from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Discipline, ProfileDisciplines, ProfileImages
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from gigma.settings import MEDIA_URL
from django.urls import is_valid_path
from urllib.parse import urlparse
from django.utils.text import slugify

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
		user_form = UserEditForm(instance=request.user,data=request.POST,prefix="user")
		profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES,prefix="profile")
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			stage_name = request.POST.get('profile-stage_name')
			stage_slug = slugify(stage_name)
			Profile.objects.filter(user_id=request.user).update(stage_slug=stage_slug)
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
	#get highest priority value
	profile = Profile.objects.get(user_id=request.user)
	try:
		max_priority = ProfileDisciplines.objects.filter(profile=profile).order_by('-profile_discipline_order').first().profile_discipline_order
	except:
		max_priority = 0

	if request.method == 'POST':
		discipline_id = request.POST.get('new_discipline')
		ProfileDisciplines.objects.create(
			profile = profile,
			discipline = Discipline.objects.get(id=discipline_id),
			skill_level = 3,
			profile_discipline_order = max_priority + 1
		)
		return redirect('edit_disciplines')

	current_disciplines_list = list(ProfileDisciplines.objects.filter(profile=profile).values_list('discipline',flat=True))
	current_disciplines = ProfileDisciplines.objects.filter(profile=profile).order_by('profile_discipline_order')
	available_disciplines = Discipline.objects.exclude(pk__in=current_disciplines_list)
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request,'account/edit_disciplines.html',{'profile':profile, 'current_disciplines':current_disciplines, 'available_disciplines':available_disciplines, 'my_profile':my_profile, 'max_priority':max_priority})

@login_required
def delete_profile_discipline(request,id=None):
	profile = Profile.objects.get(user_id=request.user)
	ProfileDisciplines.objects.filter(pk=id).delete()
	#re-order remaing PDs priority
	remaining_pds = ProfileDisciplines.objects.filter(profile=profile).order_by('profile_discipline_order')
	count = 0
	for pd in remaining_pds:
		count+=1
		pd.profile_discipline_order=count
		pd.save()
	return redirect('edit_disciplines')

@login_required
def raise_priority_profile_discipline(request,id=None):
	profile = Profile.objects.get(user_id=request.user)
	pd = ProfileDisciplines.objects.get(pk=id)
	if pd.profile_discipline_order > 1:
		pd_target_priority = pd.profile_discipline_order - 1 #1 is highest priority
		#switch priorities
		ProfileDisciplines.objects.filter(profile=profile,profile_discipline_order=pd_target_priority).update(profile_discipline_order=pd_target_priority+1)
		pd.profile_discipline_order = pd_target_priority
		pd.save()
	return redirect('edit_disciplines')

@login_required
def lower_priority_profile_discipline(request,id=None):
	profile = Profile.objects.get(user_id=request.user)
	try:
		max_priority = ProfileDisciplines.objects.filter(profile=profile).order_by('-profile_discipline_order').first().profile_discipline_order
	except:
		max_priority = 1
	profile = Profile.objects.get(user_id=request.user)
	pd = ProfileDisciplines.objects.get(pk=id)
	if pd.profile_discipline_order < max_priority:
		print('go')
		pd_target_priority = pd.profile_discipline_order + 1 #1 is highest priority
		#switch priorities
		ProfileDisciplines.objects.filter(profile=profile,profile_discipline_order=pd_target_priority).update(profile_discipline_order=pd_target_priority-1)
		pd.profile_discipline_order = pd_target_priority
		pd.save()
	return redirect('edit_disciplines')

@login_required
def edit_profile_images(request):
	#get highest priority value
	profile = Profile.objects.get(user_id=request.user)
	try:
		max_priority = ProfileImages.objects.filter(profile=profile).order_by('-image_order').first().image_order
	except:
		max_priority = 0

	if request.method == 'POST' and max_priority < 4:
		profile_img = request.FILES.get('profile_img')
		image_desc = request.POST.get('image_desc')
		print(profile_img)
		print(request.FILES)
		ProfileImages.objects.create(
			profile = profile,
			profile_image = profile_img,
			description = image_desc,
			image_order = max_priority + 1
		)
		return redirect('edit_profile_images')
	current_images = ProfileImages.objects.filter(profile=profile).order_by('image_order')
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request,'account/edit_profile_images.html',{'profile':profile, 'my_profile':my_profile, 'max_priority':max_priority, 'current_images':current_images})


@login_required
def delete_profile_images(request,id=None):
	profile = Profile.objects.get(user_id=request.user)
	ProfileImages.objects.filter(pk=id).delete()
	#re-order remaing PDs priority
	remaining_pds = ProfileImages.objects.filter(profile=profile).order_by('image_order')
	count = 0
	for pd in remaining_pds:
		count+=1
		pd.image_order=count
		pd.save()
	return redirect('edit_profile_images')

@login_required
def raise_priority_profile_images(request,id=None):
	profile = Profile.objects.get(user_id=request.user)
	pd = ProfileImages.objects.get(pk=id)
	if pd.image_order > 1:
		pd_target_priority = pd.image_order - 1 #1 is highest priority
		#switch priorities
		ProfileImages.objects.filter(profile=profile,image_order=pd_target_priority).update(image_order=pd_target_priority+1)
		pd.image_order = pd_target_priority
		pd.save()
	return redirect('edit_profile_images')

@login_required
def lower_priority_profile_images(request,id=None):
	profile = Profile.objects.get(user_id=request.user)
	try:
		max_priority = ProfileImages.objects.filter(profile=profile).order_by('-image_order').first().image_order
	except:
		max_priority = 1
	profile = Profile.objects.get(user_id=request.user)
	pd = ProfileImages.objects.get(pk=id)
	if pd.image_order < max_priority:
		pd_target_priority = pd.image_order + 1 #1 is highest priority
		#switch priorities
		ProfileImages.objects.filter(profile=profile,image_order=pd_target_priority).update(image_order=pd_target_priority-1)
		pd.image_order = pd_target_priority
		pd.save()
	return redirect('edit_profile_images')

def profile_search(request):
	profiles = Profile.objects.all().exclude(stage_name__isnull=True)
	my_profile = None
	if request.user.is_authenticated:
		my_profile = Profile.objects.get(user_id=request.user)
	return render(request, 'account/profile_search.html',{'section':'dashboard','profiles':profiles, 'my_profile':my_profile})

def profile_details(request, id, stage_slug):
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