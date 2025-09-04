from django.urls import path
from .views.users import UserView
from .views.members import MemberView
from .views.boutiques import BoutiqueListView, BoutiqueMembersView

urlpatterns = [
    path('users/api/', UserView.as_view(), name='users'),
    path('members/api/', MemberView.as_view(), name='members'),
    path('boutiques/api/', BoutiqueListView.as_view(), name='boutique-list'),
    path('boutiques/<int:boutique_id>/members/api/', BoutiqueMembersView.as_view(), name='boutique-members'),
    #path('register/boutiques/api/', RegisterBoutiqueView.as_view(), name='register-boutiques'),
]
