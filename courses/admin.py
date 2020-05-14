from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}


class VideoInline(admin.TabularInline):
    model = models.Video
    fields = ['title', 'order', ]
    readonly_fields = ['title', 'order', ]
    ordering = ['order']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class RatingInline(admin.TabularInline):
    model = models.Rating
    fields = ['user', 'rating']

    # def has_delete_permission(self, request, obj=None):
    #     return False


class ReviewInline(admin.TabularInline):
    model = models.Review
    fields = ['user', 'review']

    # def has_delete_permission(self, request, obj=None):
    #     return False


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'tutor', 'category',
                    'price', 'created']
    search_fields = ['title', 'students__user__username',
                     'tutor__user__username']
    list_filter = ['created', 'tutor']
    inlines = [VideoInline, RatingInline, ReviewInline]
    filter_horizontal = ['students']


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order', 'created']


admin.site.site_header = "MusiLearn"
admin.site.site_title = "MusiLearn Portal"
admin.site.index_title = "Welcome to MusiLearn Portal"
