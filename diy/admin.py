from django.contrib import admin
from .models import Thing, Instructions, Comment
from django_summernote.admin import (
    SummernoteModelAdmin, SummernoteModelAdminMixin)
from django.utils.html import mark_safe

NO_PARENT_NAME = "ROOT"


class ComponentInLine(SummernoteModelAdminMixin, admin.StackedInline):
    ''' Admin view for inline Componnets of a Thing   '''
    model = Thing
    fk_name = "parent"

    # Wrappers for the read-only fields, so they can be part of fieldsets
    readonly_fields = ('created', 'updated', 'parent_view')

    @admin.display(description="Created")
    def created(self, instance):
        return instance.created_on

    @admin.display(description="Modified")
    def updated(self, instance):
        return instance.updated_on

    @admin.display(description="Parent")
    def parent_view(self, instance):
        if instance.parent is None:
            return NO_PARENT_NAME
        else:
            return instance.parent

    # organize the admin inline forms fields for editting Components
    fieldsets = (
        ('Component', {
            'fields': (('parent_view', 'title', 'author', 'status'),),
        }),
        ('Description', {
            'classes': ('collapse',),
            'fields': (('slug', 'created', 'updated'), 'description',),
        }),
    )

    # No initial form displayed if no data defined
    extra = 0
    # allow to edit Component with the Thing Admin form
    show_change_link = True
    # Edit the field as WSYWYG editor
    summernote_fields = ('description')


class InstructionsInLine(SummernoteModelAdminMixin, admin.StackedInline):
    ''' Admin view for inline Instructions of a Thing/Component'''
    model = Instructions
    extra = 0   # No initial form displayed if no data defined

    # organize the admin inline forms fields for editting Instructions
    fieldsets = (
        ('Instructions', {
            'classes': ('collapse',),
            'fields': (('title',), ('instructions',),),
        }),
    )
    # allow to edit Component with the Thing Admin form
    show_change_link = True
    # Edit the field as WSYWYG editor
    summernote_fields = ('instructions')


@admin.register(Thing)
class ThingAdmin(SummernoteModelAdmin):
    ''' Admin view for Things'''
    # Displays NO_PARENT_NAME when the thing has no parent
    empty_value_display = NO_PARENT_NAME
    save_as = False
    save_as_continue = False
    save_on_top = True

    # Wrappers for the read-only fields, so they can be part of fieldsets
    readonly_fields = ('created', 'updated', 'parent_view', 'image_display')

    @admin.display(description="Created")
    def created(self, instance):
        return instance.created_on

    @admin.display(description="Modified")
    def updated(self, instance):
        return instance.updated_on

    @admin.display(description="Parent")
    def parent_view(self, instance):
        if instance.parent is None:
            return NO_PARENT_NAME
        else:
            return instance.parent

    # Prepare the featured_image to be displayed as image
    @admin.display(description="Image")
    def image_display_list(self, instance):
        return mark_safe('<img src="{}" alt ="Thing Image" style="width:100px;height:100px;object-fit:scale-down;" />'.format(instance.featured_image.url))  # noqa: E501

    @admin.display(description="Image")
    def image_display(self, instance):
        return mark_safe('<img src="{}" alt ="Thing Image" style="width:300px;object-fit:scale-down;" />'.format(instance.featured_image.url))  # noqa: E501

    # organize the list fields of Things
    list_display = ('title', 'image_display_list', 'author', 'parent_view', 'created_on', 'updated_on', 'status', )  # noqa: E501
    search_fields = ('title', 'description')
    list_filter = (
        ('parent', admin.RelatedOnlyFieldListFilter),
        'status', 'created_on'
    )
    # Allows to togle selected Things in the list between Draft and Published
    actions = ['publish', 'set_as_draft']

    def publish(self, request, queryset):
        queryset.update(status=1)

    def set_as_draft(self, request, queryset):
        queryset.update(status=0)

    # organize the admin form fields for editting a Thing
    fieldsets = (
        (None, {
            'fields': (
                ('parent_view', 'title', 'author', 'status'),
                ('slug', 'created', 'updated'),
                ('featured_image', 'image_display', 'description'),
            ),
        }),
    )

    # allows to include components and instructions to the edited Thing
    inlines = [ComponentInLine, InstructionsInLine]

    # allow for description to be edited as WSWG RTF doc
    summernote_fields = ('description')   # Edit the field as WSYWYG editor

    # fills slug field automatically from title
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Instructions)
class InstructionsAdmin(SummernoteModelAdmin):
    ''' Admin view for instructions'''
    # Displays NO_PARENT_NAME when the thing has no parent
    empty_value_display = NO_PARENT_NAME
    save_as = False
    save_as_continue = False
    save_on_top = True
    summernote_fields = ('instructions')      # Edit the field as WSYWYG editor

    # Wrappers for the read-only fields, so they can be part of fieldsets
    readonly_fields = ('created', 'updated', 'parent_view', 'image_display',
                       'thing_title')

    @admin.display(description="Created")
    def created(self, instance):
        return instance.thing.created_on

    @admin.display(description="Modified")
    def updated(self, instance):
        return instance.thing.updated_on

    @admin.display(description="Parent", ordering="thing__parent")
    def parent_view(self, instance):
        if instance.thing.parent is None:
            return NO_PARENT_NAME
        else:
            return instance.thing.parent

    @admin.display(description="Thing", ordering="thing")
    def thing_title(self, instance):
        return instance.thing.title

    @admin.display(description="Image")
    def image_display_list(self, instance):
        return mark_safe('<img src="{}" alt ="Thing Image" style="width:100px;height:100px;object-fit:scale-down;" />'.format(instance.thing.featured_image.url))  # noqa: E501

    @admin.display(description="Image")
    def image_display(self, instance):
        return mark_safe('<img src="{}" alt ="Thing Image" style="width:300px;object-fit:scale-down;" />'.format(instance.thing.featured_image.url))  # noqa: E501

    # organize the list fields of Things
    list_display = ('parent_view', 'thing_title', 'image_display_list',
                    'title')
    list_display_links = ('title',)
    search_fields = ('title', 'instructions',)
    list_filter = (
        ('thing__parent', admin.RelatedOnlyFieldListFilter),
        'thing',
    )

    # organize the admin form fields for editting Instructions
    fieldsets = (
        ('Instructions', {
            'fields': (
                ('thing', 'image_display', 'title'),
                ('instructions',),
            ),
        }),
    )


class ReplyInLine(admin.StackedInline):
    ''' Admin view for inline Replies of a Comment   '''
    model = Comment
    fk_name = "parent"

    # Wrappers for the read-only fields, so they can be part of fieldsets
    readonly_fields = ('created',)
    ordering = ['created_on']

    @admin.display(description="Created")
    def created(self, instance):
        return instance.created_on


    # organize the admin inline forms fields for editting Components
    fieldsets = (
        ('Replay', {
            'fields': (('author', 'created'),
                       'comment'),
        }),
    )

    # No initial form displayed if no data defined
    extra = 0
    # allow to edit Component with the Thing Admin form
    show_change_link = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ''' Admin view for Comment'''
    # Displays NO_PARENT_NAME when the thing has no parent
    empty_value_display = "COMMENT"
    save_as = False
    save_as_continue = False
    save_on_top = True

    # Wrappers for the read-only fields, so they can be part of fieldsets
    readonly_fields = ('created', 'parent_view')

    @admin.display(description="Created")
    def created(self, instance):
        return instance.created_on

    @admin.display(description="Comment or reply")
    def parent_view(self, instance):
        if instance.parent is None:
            return "COMMENT"
        else:
            #return instance.parent
            return "REPLAY"

    # organize the list fields of Things
    list_display = ['author', 'thing', 'created_on', 'parent_view']
    search_fields = ['author', 'thing', 'comment']
    list_filter = (
        'author',
        'thing',
        'created_on'
    )

    # organize the admin form fields for editting a Thing
    fieldsets = (
        (None, {
            'fields': (
                ('parent_view',),
                ('created', 'author', 'thing'),
                ('comment',),
            ),
        }),
    )

    # allows to include replies to be added to the edited comment
    inlines = [ReplyInLine,]
