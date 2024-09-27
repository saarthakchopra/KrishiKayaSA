from django.urls import path
from . import views

urlpatterns = [
    path('',views.marketPlace.as_view(), name = 'market-place'),
    path('register/',views.SignUpView.as_view(), name = 'register'),
    path('login/',views.UserLoginPageView.as_view(), name = 'login'),
    path('logout/',views.logoutUser, name = 'logout'),
    path('dashboard/',views.StockList.as_view(), name = 'dashboard'),
    path('dashboard/item/<int:pk>/',views.ItemDetail.as_view(), name = 'item-detail'),
    path('dashboard/item-create/',views.CreateItem.as_view(), name = 'create-item'),
    path('dashboard/item-update/<int:pk>/',views.UpdateItem.as_view(), name = 'update-item'),
    path('dashboard/item-delete/<int:pk>/',views.DeleteItem.as_view(), name = 'delete-item'),
    path('dashboard/analytics/',views.analytics, name = 'analytics'),
]