from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from .forms import PostForm,CommentForm
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
        return redirect('post_detail', slug=post.slug)
    return render(request, 'post/create_post.html', {'form': form})

def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created')
    profile = user.profile  # Assuming you have a Profile model with image

    return render(request, 'user_posts.html', {
        'profile_user': user,
        'posts': posts,
        'profile': profile,
    })


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return redirect('post_detail', slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_detail', slug=post.slug)
    return render(request, 'post/edit_post.html', {'form': form})

def post_list(request):
    posts = Post.objects.all().order_by('-created')
    paginator = Paginator(posts, 5)  # 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'post/post_list.html', {'posts': posts})

@require_POST
@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    return redirect('post_detail', slug=slug)

@require_POST
@login_required
def dislike_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.dislikes.add(request.user)
    post.likes.remove(request.user)
    return redirect('post_detail', slug=slug)



def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.order_by('-created')
    form = CommentForm()

    if request.method == 'POST' and post.allow_comments:
        form = CommentForm(request.POST)
        if form.is_valid():
            last_comment = Comment.objects.filter(user=request.user).order_by('-created').first()
            if not last_comment or timezone.now() - last_comment.created > timedelta(seconds=30):
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', slug=slug)

    return render(request, 'post/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return redirect('post_detail', slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'post/delete_post.html', {'post': post})
