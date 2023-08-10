from django.urls import re_path
from . import views

urlpatterns = [
    re_path('signup', views.signup),
    re_path('signin', views.signin),
    re_path('test', views.test),
    re_path('logout', views.logout_view),
    re_path('', views.log_template),
]
