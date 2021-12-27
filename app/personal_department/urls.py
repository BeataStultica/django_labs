from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('persons/', views.get_persons_list, name='persons-list'),
    path('persons/create', views.create_person, name='persons-create'),
    path('persons/<int:person_id>', views.get_persons_by_id, name='person-detail'),
    path('persons/<int:person_id>/update', views.update_person_by_id, name='person-update'),
    path('persons/<int:person_id>/delete', views.delete_person_by_id, name='person-delete'),
]
