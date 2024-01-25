from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostEmail
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
# def post_list(request):
#     posts=Post.published.all()
#     return render(request,'blog/post/list.html',{'posts':posts})
class PostListView(ListView):
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=3
    template_name='blog/post/list.html'

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,
                           status=Post.Status.PUBLISHED,
                           slug=post,
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)
    return render(request,'blog/post/detail.html',{'post':post})

def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent=False
    if request.method=='POST':
        form=EmailPostEmail(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url = request.build_absolute_uri(
            post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER,
            [cd['to']])
            sent = True
    else:
        form=EmailPostEmail()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent': sent})













