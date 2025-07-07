from django.contrib import admin
from .models import RegisteredUser, GuestUser, PopQuiz, Presentation

admin.site.register(RegisteredUser)
admin.site.register(GuestUser)
admin.site.register(PopQuiz)
admin.site.register(Presentation)
