from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('/expand', views.expand_row, name="expand_row"),
]