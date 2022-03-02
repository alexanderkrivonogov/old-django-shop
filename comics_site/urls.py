from django.urls import path

from comics_site import views


urlpatterns = [
    path('', views.comics_list, name='comics_list'),
    path('<category_slug>', views.comics_list, name='comics_list_by_category'),
    path('<id>/<slug>', views.comics_detail, name='comics_detail'),

]
