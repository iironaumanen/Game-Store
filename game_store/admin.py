from django.contrib import admin
from .models import Game, StoreUser, Category, Score, Save

admin.site.register(Game)
admin.site.register(StoreUser)
admin.site.register(Category)
admin.site.register(Score)
admin.site.register(Save)
