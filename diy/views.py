from django.shortcuts import render, HttpResponse, get_object_or_404, reverse
from django.views import generic, View
from .models import Thing, Instructions
from django.http import HttpResponseRedirect


class ThingList(generic.ListView):
    ''' Provides de list of Things objects'''
    model = Thing
    queryset = Thing.objects.filter(status=1, parent=None).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


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
            if thing.likes.filter(id=self.request.user.id).exists():
                liked = True
            is_component_thing={}
            for i in components:
                 is_component_thing[i.id]=Instructions.objects.filter(thing=i.id).exists()
            return render(
                request,
                "thing_detail.html",
                {
                    "thing": thing,
                    "components": components,
                    "instructions": instructions,
                    "is_component_thing": is_component_thing,
                    "liked": liked
                },
            )   

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
    def get(self, request, form,  *args, **kwargs):
            print (f"form={form}, user={request.user.__dict__}")
            return render(
                request,
                "user_profile.html",
            )   
        