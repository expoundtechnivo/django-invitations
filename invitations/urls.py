from django.urls import path

from . import views

app_name = 'invitations'
urlpatterns = [
    path('send-invite/', views.SendInvite.as_view(),
        name='send-invite'),

    path('send-json-invite/', views.SendJSONInvite.as_view(),
        name='send-json-invite'),

    path('accept-invite/<slug:key>', views.AcceptInvite.as_view(),
        name='accept-invite'),
]
