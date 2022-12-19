from django.contrib import admin
from .models import Post, Profile, Thread, Message

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    fields = ['post_title', 'post_text', 'favorite']

class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'year', 'major', 'friends']

class ThreadAdmin(admin.ModelAdmin):
    fields = ['user1', 'user2', 'was_read']

class MessageAdmin(admin.ModelAdmin):
    fields = ['thread', 'sender', 'receiver', 'message_text', 'was_read']

admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)

