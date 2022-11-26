from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.signIn, name='login'),
    path('login/error', views.loginError, name='login_error'),
    path('logout/', views.logOut, name='logout'),
    path('register/', views.signUp, name='register'),
    path('register/success', views.signUpSuccess, name='register_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-restaurant/', views.addRestaurant, name='add_restaurant'),
    path('dashboard/restaurant/<slug:slug>/', views.displayRestaurant, name='view_restaurant'),
    path('dashboard/restaurant/<slug:slug>/add-dish/', views.addDish, name='add_dish'),
    path('dashboard/restaurants/', views.displayRestaurants, name='display_restaurants'),
    path('dashboard/restaurants/<slug:slug>/', views.makeOrder, name='make_order'),
    path('dashboard/order/', views.viewPlacedOrder, name='order'),
    path('dashboard/order/<int:order_id>/', views.displayOrder, name='display_order'),
    path('dashboard/order/<int:order_id>/review', views.displayReview, name='display_review'),
]