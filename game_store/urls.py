"""game_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from . import views
from .views import api_games

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('', views.main_page),
    path('home/', views.main_page),
    path('account/', include('django.contrib.auth.urls')),
    path('game/', views.game_search),
    path('hiscores/', views.hiscores_choose),
    path('about/', views.about),
    path('own_game/', views.own_game),
    path('hiscores/<str:game_title>', views.hiscores),
    path('category/<str:category_title>', views.game_category),
    path('game/<str:game_title>', views.game_page),
    path('game_not_owned/', views.game_not_owned),
    re_path('api/(?P<version>(v1|v2))/games', api_games.as_view(), name='games'),
    re_path('api/(?P<version>(v1|v2))/score', views.save_game_score, name='games'),
    re_path('api/(?P<version>(v1|v2))/save', views.save_game_state),
    re_path('api/(?P<version>(v1|v2))/load', views.load_game_state),
    path('payment/<str:payment_result>/', views.payment_handler),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('dev/', views.developer),
    path('dev/my_games/', views.my_games),
    path('dev/modify_game/<str:game_title>', views.modify_game),
    path('dev/add_game/', views.add_game),
    path('dev/add_game/submit/', views.add_game_submit),
    path('dev/remove_game/<str:game_title>', views.remove_game),
    path('dev/convert_to_developer/', views.convert_to_developer),
    path('dev/sales/<str:game_title>', views.game_sales),
]
