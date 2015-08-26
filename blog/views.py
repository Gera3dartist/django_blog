from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Post, Choices
# Create your views here.


def index(request):
    latest_post = Post.objects.order_by('-created')
    context = {'latest_post': latest_post}
    return render(request, 'blog/index.html', context)


def details(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def created(request, post_id):
    post = Post.objects.get(id=post_id)
    return HttpResponse(post.created)


def vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    try:
        selected_choice = post.choices_set.get(pk=request.POST['choice'])
    except (KeyError, Choices.DoesNotExist):
        # render post voting form
        return render(request, 'blog/detail.html', {
            'post': post,
            'error_message': 'You did note select a choice'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('blog:results', args=(post.id,)))


def results(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/result.html', {'post': post})



