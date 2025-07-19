from django.contrib import admin
from .models import *

admin.site.register(RegisteredUser)
admin.site.register(PopQuiz)
admin.site.register(Presentation)
admin.site.register(MediaFile)
admin.site.register(PresentationParticipant)


