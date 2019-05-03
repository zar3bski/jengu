from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('record/', views.record_session, name='record_session'),
    path('profile/', views.Profile.as_view(), name='profil'),

    path('save/', views.Save.as_view(), name='save'),
    path('save/?=patients', views.Save.as_view(), name='save'),
    path('save/?=consultations/', views.Save.as_view(), name='save'),

    path('browse/',views.browse, name='browse'),
    path('compta/',views.Compta.as_view(), name='compta'),
    path('compta/<int:month>/',views.ComptaDetail.as_view(), name='compta_detail'),
    path('browse/<int:patient_id>/', views.Detail.as_view(), name='detail'),
    path('browse/<int:patient_id>/edit_note/', views.edit_note),
    path('browse/<int:patient_id>/edit_patient/', views.edit_patient),
]


