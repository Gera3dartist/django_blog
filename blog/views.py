from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Choices
from django.views import generic
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_post'

    def get_queryset(self):
        return Post.objects.filter(
            created__lte=timezone.now()
        ).order_by('-created')[:5]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['count'] = Post.objects.count()
        return context


class DetailsView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'


class ResultsView(generic.DetailView):
    model = Post
    template_name = 'blog/result.html'


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


def created(request, post_id):
    post = Post.objects.get(id=post_id)
    return HttpResponse(post.created)
