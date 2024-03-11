from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import generic, View
from .models import Thing


class ThingList(generic.ListView):
    model = Thing
    queryset = Thing.objects.filter(status=1, parent=None).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6

class ThingDetail(View):
    def get(self, request, slug, *args, **kwargs):
            queryset = Thing.objects.filter(status=1, parent = None)
            thing = get_object_or_404(queryset, slug=slug)
            print(f"thing={thing.title}")
            instructions = thing.instructions.order_by("title")
            components = thing.components.filter(status=1).order_by("title")
            liked = False
            if thing.likes.filter(id=self.request.user.id).exists():
                liked = True
            print(f"Components: {components}")
            for step in instructions:
                print(f"Step: {step.title}, Instructions:{step.instructions}")
            return render(
                request,
                "thing_detail.html",
                {
                    "thing": thing,
                    "components": components,
                    "instructions": instructions,
                    "liked": liked
                },
            )    
        