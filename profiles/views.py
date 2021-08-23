from django.contrib import messages
from django.contrib.auth import logout, views, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Profile
from django.views.generic import TemplateView, FormView, UpdateView
from NEWS_WEBAPP.forms import CustomRegisterForm, CustomEditProfileForm, ProfileForm, CustomLoginForm


def login_register(request):
    if request.method == 'POST':
        register_form = CustomRegisterForm(request.POST)
        if 'signup' in request.POST:
            if register_form.is_valid():
                register_form.save()
                messages.success(request, f'Tạo tài khoản thành công !')
                new_user = authenticate(username=register_form.cleaned_data['username'],
                                        password=register_form.cleaned_data['password1'], )
                login(request, new_user)
                return redirect("login")
            else:
                email = register_form.cleaned_data.get('email')
                password1 = register_form.cleaned_data.get('password1')
                password2 = register_form.cleaned_data.get('password2')
                if password1 == password2:
                    messages.error(request, f'Tên tài khoản đã tồn tại')
                    return redirect('login')
                else:
                    messages.error(request, "Mật khẩu xác thực không khớp")
                    return redirect('login')
        elif 'login' in request.POST:
            log_view = views.LoginView.as_view(template_name='login.html')
            log_view(request)
            if request.user.is_authenticated:
                messages.success(request, 'Đăng nhập thành công')
            else:
                messages.error(request, 'Tài khoản không tồn tại')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('profile')
        else:
            register_form = CustomRegisterForm()
            login_form = CustomLoginForm(request)
            return render(request, 'login.html', {'register_form': register_form, 'login_form': login_form})


class LogoutSite(LogoutView):
    template_name = 'profile.html'


class ProfileSite(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


@login_required
def update_profile(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = CustomEditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Cập nhật tài khoản thành công')
            return redirect('profile')
        else:
            messages.error(request, 'Vui lòng điền đúng định dạng')
    else:
        user_form = CustomEditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class PasswordChange(PasswordChangeView):
    from_class = PasswordChangeView
    template_name = 'pass_change.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        self.request.session.flush()
        logout(self.request)
        messages.success(self.request, 'Đổi mật khẩu thành công')
        return super().form_valid(form)


# class LoginSite(SuccessMessageMixin, LoginView):
#     template_name = 'base.html'
#     redirect_authenticated_user = True
#     success_message = "Logged in successfully"

#
# class RegisterSite(FormView):
#     template_name = 'register.html'
#     form_class = CustomRegisterForm
#
#     def form_valid(self, form):
#         data = form.cleaned_data
#         new_user = User.objects.create_user(
#             username=data['username'],
#             password=data['password1'],
#             email=data['email']
#         )
#         messages.success(self.request, 'Register successful')
#         return redirect('login')

# class EditProfile(generic.UpdateView):
#     model = User
#     form_class = CustomEditProfileForm
#     template_name = "edit_profile.html"
#     success_url = '/profile/'
#
#     def get_object(self):
#         return self.request.user
#
#
# class BioProfileView(generic.UpdateView):
#     model = Profile
#     fields = ('bio', 'avatar', 'media_url')
#     template_name = 'bio_profile.html'
#     success_url = '/profile/'
#
#     def get_object(self):
#         return self.request.user
