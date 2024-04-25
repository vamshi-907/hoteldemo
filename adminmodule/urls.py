from django.urls import path
from . import views

urlpatterns = [
    path('add_hotel/', views.add_hotel, name='add_hotel'),
    path('view_hotels/', views.view_hotels, name='view_hotels'),
    path("delete_hotel/<int:pk>", views.delete_hotel, name='delete_hotel'),
    path('search/', views.search_view, name='search'),
    path('adminhomepage', views.adminhomepage, name='adminhomepage'),
    path('edit_hotel/<int:pk>',views.edit_hotel,name='edit_hotel'),
    path('hoteloverview/<int:hotel_id>',views.hoteloverview,name='hoteloverview'),
    path('payment-status', views.paymentstatus, name='payment-status'),
    path('hotel_payment',views.hotelpaymentmodule,name='hotel_payment'),
]
