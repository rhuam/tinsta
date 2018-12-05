from django.contrib import admin
from .models import UserFace, UserInsta, UserTinder, People, PhotosPeople

admin.site.register(UserFace)
admin.site.register(UserInsta)
admin.site.register(UserTinder)
admin.site.register(People)
admin.site.register(PhotosPeople)