from django.contrib import admin
from TestApp.models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'body', 'publish', 'created', 'updated', 'status']
    list_filter = ('status', 'author', 'created', 'publish')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
