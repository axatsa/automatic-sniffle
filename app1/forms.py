from django import forms
from django.contrib.auth.models import User
from .models import Video, Comment, Profile


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Create Profile
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number')
            )
        return user


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_title', 'video_content', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'rows': 3}),
        }