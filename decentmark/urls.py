from django.urls import path
from decentmark import views

app_name = 'decentmark'

urlpatterns = [
    path('', views.unit_list, name="unit_list"),
    path('unit/create/', views.unit_create, name="unit_create"),
]
