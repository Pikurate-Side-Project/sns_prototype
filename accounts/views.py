from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('root')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })