from django.db import models
from django.conf import settings
from django.urls import reverse

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "users/{0}/{1}".format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    website_link = models.TextField(blank=True, null=True)
    user_about = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    account_type = models.CharField(max_length=3,choices={"ART":"Artist","ORG":"Organiser","PUB":"Public"},null=True)
    stage_slug = models.SlugField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ['stage_name']
        indexes = [models.Index(fields=['stage_name'])]

    def __str__(self):
        return self.stage_name
    
    def get_absolute_url(self):
        return reverse('profile_details',args=[self.id,self.stage_slug])


class Discipline(models.Model):
    discipline_name = models.CharField(max_length=100)
    discipline_icon = models.ImageField(upload_to='icons/', blank=True)
    parent_discipline = models.ForeignKey('self',related_name='child_discipline',on_delete=models.SET_NULL,null=True,blank=True) #will be null if discipline is top level

    def __str__(self):
        return self.discipline_name

class ProfileDisciplines(models.Model):
    #intermediate table saves relationships between disciplines and user profiles
    profile = models.ForeignKey(Profile,related_name='profile_disciplines', on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline,related_name='discipline_profiles', on_delete=models.CASCADE)
    skill_level = models.PositiveSmallIntegerField(
        choices=(
            (1,"Beginner"),
            (2,"Intermediate"),
            (3,"Advanced")
        )
    )
    profile_discipline_order = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

def user_directory_path_image(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print('go')
    return "users/{0}/{1}".format(instance.profile.user.id, filename)

class ProfileImages(models.Model):
    profile = models.ForeignKey(Profile,related_name='profile_images', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=user_directory_path_image, blank=True, null=True)
    description = models.TextField(null=True)
    image_order = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)