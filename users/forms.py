from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'autocomplete': 'off'}))
    mobile = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "mobile", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['password1'].widget.attrs.update({'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'autocomplete': 'new-password'})
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Update the profile with mobile number
            from users.models import Profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data["mobile"]
            profile.save()
        return user

class EmployeeRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('washer', 'Washer'),
        ('supervisor', 'Supervisor'),
    ]
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "mobile", "role", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.is_active = False  # Inactive until approved
        if commit:
            user.save()
            from users.models import Profile
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data["mobile"],
                role=self.cleaned_data["role"],
                is_approved=False
            )
        return user
