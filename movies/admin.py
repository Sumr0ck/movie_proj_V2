from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Register your models here.
class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ['name']


class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 0
    readonly_fields = ('title', 'description', 'image', 'get_image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height="60">')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url', 'draft']
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInLine, ReviewInLine]
    save_on_top = True
    save_as = True
    form = MovieAdminForm
    actions = ('published', 'unpublished')
    list_editable = ('draft', )
    readonly_fields = ('get_poster', )
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'), )
        }),
        (None, {
            'fields': ('description', ('get_poster', 'poster'))
        }),
        (None, {
            'fields': (('year', 'world_premier', 'country'), )
        }),
        ('Actors', {
            'classes': ('collapse', ),
            'fields': (('actors', 'directors', 'genres', 'category'), )
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'), )
        }),
        ('Options', {
            'fields': (('url', 'draft'), )
        })
    )

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="110">')

    def published(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была опубликованна'
        else:
            message_bit = f'{row_update} записей было опубликованно'
        self.message_user(request, message_bit)

    def unpublished(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была снята с публикации'
        else:
            message_bit = f'{row_update} записей было снято с публикации'
        self.message_user(request, message_bit)

    get_poster.short_description = 'Постер'

    published.short_description = 'Опубликовать'
    published.allowed_permissions = ('change', )

    unpublished.short_description = 'Снять с публикации'
    unpublished.allowed_permissions = ('change', )

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'star', 'ip')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height="60">')

    get_image.short_description = 'Изображение'


admin.site.register(RatingStar)
admin.site.site_title = 'Django movies'
admin.site.site_header = 'Django movies'