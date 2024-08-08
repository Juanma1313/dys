from django.shortcuts import (
    render, HttpResponse, get_object_or_404, reverse, redirect)
from django.views import generic, View
from .models import Thing, Instructions, Comment
from django.http import HttpResponseRedirect
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class ThingList(generic.ListView):
    ''' Provides de list of Things objects'''
    model = Thing
    queryset = Thing.objects.filter(status=1, parent=None).order_by('-created_on')  # noqa: E501
    template_name = 'index.html'
    paginate_by = 6
    print("ThingList Done")


class ThingDetail(View):
    ''' Provides with the details for the selected thing.
    it also creates a dictionary is_component_thing that indicates if there are
    nested instructions in any of the Thing's Components'''
    def get(self, request, slug, *args, **kwargs):
        queryset = Thing.objects.filter(status=1)
        thing = get_object_or_404(queryset, slug=slug)
        instructions = thing.instructions.order_by("title")
        components = thing.components.filter(status=1).order_by("title")
        liked = False
        comments = Comment.objects.filter(thing=thing)

        if thing.likes.filter(id=self.request.user.id).exists():
            liked = True
        is_component_thing = {}
        for i in components:
            is_component_thing[i.id] = Instructions.objects.filter(thing=i.id).exists()  # noqa: E501
        return render(
            request,
            "thing_detail.html",
            {
                "thing": thing,
                "components": components,
                "instructions": instructions,
                "is_component_thing": is_component_thing,
                "liked": liked,
                "comments": comments,
                "comment_count": comments.count(),
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        if self.request.method == 'POST':
            if not request.user.is_authenticated:
                messages.add_message(
                    request, messages.ERROR,
                    'You need to be Signed in to post comments!')
            else:
                comment_form = CommentForm(self.request.POST)
                if comment_form.is_valid():
                    comment = comment_form.cleaned_data['comment']
                    try:
                        parent = comment_form.cleaned_data['parent']
                    except Exception:
                        parent = None

                    thing = get_object_or_404(Thing, slug=slug)
                    new_comment = Comment(comment=comment,
                                          author=self.request.user,
                                          thing=thing,
                                          parent=parent)
                    new_comment.save()
                    messages.add_message(
                        request, messages.SUCCESS, 'Comment Added!')
                else:
                    messages.add_message(
                        request, messages.ERROR, 'Error adding Comment!')

        return redirect(self.request.path_info)


class ThingLike(View):
    ''' This view allows for adding/removing a user Like to/from a Thing.
    If the user like already exists it removes it otherwise it adds it '''
    def post(self, request, slug, *args, **kwargs):
        thing = get_object_or_404(Thing, slug=slug)
        if thing.likes.filter(id=request.user.id).exists():
            thing.likes.remove(request.user)
        else:
            thing.likes.add(request.user)

        return HttpResponseRedirect(reverse('thing_detail', args=[slug]))


class UserProfile(View):
    ''' Provides with the details for the user profile'''
    def get(self, request, form, *args, **kwargs):
        return render(
            request,
            "user_profile.html",
        )


@login_required
def comment_edit(request, slug, comment_id):
    ''' This view allows for edditing a user comment from a Thing.
    User must be logged in and be superuser or author of the comment
    '''

    if request.method == "POST":

        comment = get_object_or_404(Comment, id=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)
        parent_id = comment.parent_id  # Preserve the parent

        if comment_form.is_valid() and (
                request.user.is_superuser or comment.author == request.user):
            comment.parent_id = parent_id  # restore original parent
            comment = comment_form.save(commit=False)
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating comment!')

    return HttpResponseRedirect(reverse('thing_detail', args=[slug]))


@login_required
def comment_delete(request, slug, comment_id):
    ''' This view allows for deleting a user comment from a Thing.
    User must be logged in and be superuser or author of the comment
    '''
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user.is_superuser or comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'You cannot delete this comment!')

    return HttpResponseRedirect(reverse('thing_detail', args=[slug]))
