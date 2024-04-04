from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.base_view, name="base_view"),
    path('signupForm_view', views.signupForm_view, name="signupForm_view"),
    path('index_view', views.index_view, name="index_view"),
    path('login_view', views.login_view, name="login_view"),
    path('logout_view', views.logout_view, name="logout_view"),
    path('add_friend', views.add_friend, name="add_friend"),
    path('friend_view/<str:f_uid>/', views.friend_view, name="friend_view"),
    path('friend_view/<str:f_uid>/add_expense_record', views.add_expense_record, name='add_expense_record'),
    path('add_group', views.add_group, name="add_group"),
    path('group_view/<str:gname>/', views.group_view, name="group_view"),
    path('group_view/<str:gname>/add_group_members', views.add_group_members, name="add_group_members"),
    path('group_view/<str:gname>/add_group_expense_record', views.add_group_expense_record, name="add_group_expense_record"),
    path('show_expenses/', views.show_expenses, name="show_expenses"),
    path('show_settlement_view/settlement_view', views.settlement_view, name="settlement_view"),
    path('show_settlement_view/', views.show_settlement_view, name="show_settlement_view"),
]