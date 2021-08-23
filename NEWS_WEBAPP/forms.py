from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from blogs.models import Post, Comment
from profiles.models import Profile


class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(label='Tài khoản', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control',}) , required=True)
    first_name = forms.CharField(label='Họ', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(label='Tên', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control'}) , required=True)
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control'}) , required=True)
    password2 = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control'}) , required=True)

    class Meta:
        model = User
        fields = ("username", "email", 'first_name', 'last_name', 'password1', 'password2')
        field_classes = {'username': UsernameField}
        help_texts = {
            'username': None,
            'password2': None,
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Tài khoản', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}) , required=True)
    password = forms.CharField(label='Mật Khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control'}) , required=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class CustomEditProfileForm(forms.ModelForm):
    username = forms.CharField(label='Tài khoản', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control' , 'readonly':'readonly'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}) , required=True)
    first_name = forms.CharField(label='Họ', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}) , required=True)
    last_name = forms.CharField(label='Tên', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control'}) , required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(label='Tiểu sử', required=False,
                          widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 15}))
    avatar = forms.ImageField(label='Ảnh Profile',widget=forms.FileInput)
    media_url = forms.CharField(label='Mạng xã hội', max_length=300, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ('bio', 'media_url', 'avatar')


class CommentForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}) , required=True)
    body = forms.CharField(label='Write comment',
                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 15}) , required=True)

    class Meta:
        model = Comment
        fields = ('author', 'name', 'body' )


class CustomPostForm(forms.ModelForm):
    title = forms.CharField(label='Tiêu đề', widget=forms.TextInput(attrs={'class': 'form-control'}) , required=True)
    body = forms.CharField(label='Nhập nội dung bài viết: ', required=True,
                           widget=CKEditorUploadingWidget)
    image = forms.ImageField(label='Ảnh thumbnail: ', required=True, widget=forms.ClearableFileInput)

    class Meta:
        model = Post
        fields = ('title','image','body')
