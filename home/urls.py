# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
# ]



from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("base/", views.base, name="base"),
    path("connect/", views.contact, name="contact"),
]

