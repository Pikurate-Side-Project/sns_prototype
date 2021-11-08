from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post, Tag
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

def post_detail(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
    except Post.DoesNotExist:
        raise Http404('해당 모델이 존재하지 않습니다.')

    return render(request, 'feeds/post_detail.html', {
        'post': post,
    })