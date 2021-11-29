from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.search, name="search"),
    path('category/<str:pk>', views.getCategory, name='category'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('book/<str:pk>', views.getBook, name="getbook"),
    path('writer/<str:pk>', views.getWriter, name="getwriter"),
    path('delete-review/<str:pk>', views.deleteReview, name="deleteReview"),
    path('fav/<str:pk>', views.fav_add, name='fav_add'),
    path('fav_book/', views.fav_book, name='fav_book'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order')
]