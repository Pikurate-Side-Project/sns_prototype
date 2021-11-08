from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Tag
from .forms import PostForm

# Create your views here.
@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, '새 포스팅이 저장되었습니다.')
            return redirect('root') # TODO: get_absolute_url 활용
    else:
        form = PostForm()

    return render(request, 'feeds/post_new_form.html', {
        'form': form,
    })