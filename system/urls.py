from django.urls import path
from .views import (
    home,
    page,
    index,
    CreateView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name="home"),
    path('index/',index,name="index"),
    path('page/',page,name="page"),
    path('create-course/',CreateView.as_view(),name="create-course"),
]
urlpatterns+=static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
