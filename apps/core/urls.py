from django.urls import path

from apps.core import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('analyse', views.AnalyseView.as_view(), name='analyse'),
    path('images', views.ImageListView.as_view(), name='image_list'),
    path('image/<int:pk>', views.ImageDetail.as_view(), name='image_detail'),
]
