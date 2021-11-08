from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, logout_then_login, 
    PasswordChangeView as AuthPasswordChangeView,
)

from .forms import (
    PasswordChangeForm, ProfileForm, SignupForm,
)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            signed_user = form.save()
            signed_user.send_welcome_email() # FIXME: Celery로 처리하기
            auth_login(request, signed_user)
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('root')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })

login = LoginView.as_view(template_name='accounts/login_form.html')

def logout(request):
    messages.success(request, '로그아웃이 되었습니다.')
    return logout_then_login(request)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필 수정이 완료되었습니다.')
            return redirect('accounts:profile_edit')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile_edit.html', {
        'form': form,
    })

class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy('accounts:password_change')
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, '암호를 변경했습니다.')
        return super().form_valid(form)

password_change = PasswordChangeView.as_view()