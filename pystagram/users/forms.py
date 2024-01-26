from django import forms

#추가
from django.core.exceptions import ValidationError
from users.models import User
#추가
from django.contrib.auth.forms import UserChangeForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _




class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        widget=forms.TextInput(
            attrs={"placeholder": "사용자명 (3자리 이상)"},
        ),
    )
    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호 (4자리 이상)"},
        ),
    )

    class Meta:
        model = User

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if user:
                if user.login_attempts >= 5:  # 로그인 시도 횟수 제한을 5으로 설정
                    raise forms.ValidationError("로그인 시도 횟수가 초과되었습니다. 2단계 인증 및 관리자에게 문의하세요.")
                if not user.check_password(password):
                    user.login_attempts += 1
                    user.save()
                    error_message = f"잘못된 비밀번호입니다. 로그인 시도 횟수: {user.login_attempts}/5"
                    raise forms.ValidationError(error_message)
            return super().clean()

class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    profile_image = forms.ImageField()
    short_description = forms.CharField()

    #추가
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"입력한 사용자명({username})은 이미 사용 중. ")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"입력한 이메일은({email})은 이미 사용 중. ")
        return email

    # 추가
    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            self.add_error("password2", "비밀번호가 확인 해주세요.")

    def save(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password1 = self.cleaned_data["password1"]
        profile_image = self.cleaned_data["profile_image"]
        short_description = self.cleaned_data["short_description"]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            profile_image=profile_image,
            short_description=short_description,
        )
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ['email', 'short_description', 'profile_image']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="이메일",
    )