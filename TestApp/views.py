from django.shortcuts import render, get_object_or_404
from TestApp.models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView

# Create your views here.


def post_list_view(request):
    post_list = Post.object.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'testApp/post_list.html', {'post_list': post_list})


class PostListView(ListView):
    model = Post
    paginate_by = 2


def post_detail_view(request, year, month, day, post):
    Post_data = get_object_or_404(Post, status='published', publish__year=year, publish__month=month, publish__day=day)

    return render(request, 'testApp/post_detail.html', {'post': Post_data})


from django.core.mail import send_mail
from TestApp.forms import EmailSendForm


def mail_send_view(request, id):
    post = get_object_or_404(Post, id=id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = '{}({}) recommends you to read"{}"'.format(cd['name'], cd['email'], post.title)
            post_path = post.get_absolute_path()
            message = 'Read post At:\n {}\n\n{}\'s Comments:\n{}'.format(post_path, cd['name'], cd['comments'])
            send_mail(subject, message, 'geetanjali.umarani12@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailSendForm()
    return render(request, 'testApp/sharebymail.html', {'form': form})
