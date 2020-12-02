from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('vote/', views.vote, name='vote'),
    path('<int:answer_id>/results/', views.results, name='results'),
]
