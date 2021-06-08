from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('about_us', views.about_us),
    path('home', views.home),
    path('post_review', views.post_review),
    path('post_comment/<int:id>', views.post_comment),
    path('user_profile/<int:id>', views.profile),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment),
    path('delete_review/<int:id>', views.delete_review),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('review_page/<int:id>', views.review_page),
    path('review_types', views.review_types),
]