from django.contrib import admin
from .models import Thing, Instructions
from django_summernote.admin import SummernoteModelAdmin, SummernoteModelAdminMixin


class ComponentInLine(SummernoteModelAdminMixin, admin.StackedInline):
    model = Thing
    fk_name = "parent"
    fieldsets = (
        ('Componente', {
            'fields': (('parent_view', 'title', 'author', 'status'),),
        }),
        ('Description', {
            'classes': ('collapse',),
            'fields': (('slug', 'created', 'updated'), 'description',),
        }),
    )

    extra = 0
    show_change_link=True
    summernote_fields=('description')
    readonly_fields = ('created', 'updated','parent_view')
    @admin.display(description="Created")
    def created(self, instance):
        return(instance.created_on)

    @admin.display(description="Modified")
    def updated(self, instance):
        return(instance.updated_on)

    @admin.display(description="Parent")
    def parent_view(self, instance):
        if instance.parent is None:
            return "Root"
        else:
            return instance.parent


class ThingInstructions(SummernoteModelAdminMixin, admin.TabularInline):
    model = Instructions
    extra = 0
    summernote_fields=('instructions')

@admin.register(Thing)
class ThingAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'author', 'parent_view', 'created_on', 'updated_on', 'status')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': (('parent_view', 'title', 'author', 'status'),('slug', 'created', 'updated'), 'description',),
        }),
    )
    inlines = [ComponentInLine, ThingInstructions]
    summernote_fields=('description')
    prepopulated_fields={'slug': ('title',)}
    empty_value_display= '*** ROOT ***'
    #ordering = ['parent']
    list_filter = (
        #('parent', admin.EmptyFieldListFilter), 
        ('parent', admin.RelatedOnlyFieldListFilter), 
        'status', 'created_on'
    )
    readonly_fields = ('created', 'updated','parent_view')
    @admin.display(description="Created")
    def created(self, instance):
        return(instance.created_on)

    @admin.display(description="Modified")
    def updated(self, instance):
        return(instance.updated_on)

    @admin.display(description="Parent")
    def parent_view(self, instance):
        if instance.parent is None:
            return "*** ROOT *** "
        else:
            return instance.parent

    actions =['publish', 'set_as_draft']

    def publish(self, request, queryset):
        queryset.update(status=1)

    def set_as_draft(self, request, queryset):
        queryset.update(status=0)
     

@admin.register(Instructions)
class InstructionsAdmin(SummernoteModelAdmin):
    fieldsets = []
    summernote_fields=('instructions')


#admin.site.register(Thing, ThingAdmin)
#admin.site.register(Thing)
#admin.site.register(Instructions)
