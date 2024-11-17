from django import forms
from django.contrib.auth.models import User
from .models import Profile
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from io import BytesIO
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserRegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-profileEdit'
        self.helper.form_method = 'post'
        self.helper.form_action = 'edit_disciplines'

        self.helper.add_input(Submit('submit', 'Submit'))

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['stage_name', 'date_of_birth', 'website_link', 'user_about', 'profile_picture']

    def clean_profile_picture(self):
        print(self.cleaned_data['profile_picture'])
        im = Image.open(self.cleaned_data['profile_picture'])
        thumb_width = 500

        def crop_center(pil_img, crop_width, crop_height):
            img_width, img_height = pil_img.size
            return pil_img.crop(((img_width - crop_width) // 2,
                                (img_height - crop_height) // 2,
                                (img_width + crop_width) // 2,
                                (img_height + crop_height) // 2))
        
        def crop_max_square(pil_img):
            return crop_center(pil_img, min(pil_img.size), min(pil_img.size))
        
        
        im_thumb = crop_max_square(im).resize((thumb_width, thumb_width), Image.LANCZOS)
        buffer = BytesIO()
        im_thumb.save(fp=buffer, format='PNG')
        im_final = ContentFile(buffer.getvalue())

        image_field = self.instance.profile_picture
        image_name = 'profile_picture.png'
        image_field.delete(save=True)
        image_field.save(image_name, InMemoryUploadedFile(
                                            im_final,
                                            None,
                                            image_name,
                                            'image/png',
                                            im_final.tell,
                                            None,
                                            None
                                            )
                        )