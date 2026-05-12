from django.urls import path
from . import views

urlpatterns=[
    
    path('blogs/', views.blog_page, name='blog_page'),
    path('create/',views.create_post,name='create_post'),
    path('delete/<int:id>/',views.delete_blog,name='delete_blog'),
    path('edit/<int:id>/',views.edit_blog,name='edit_blog'),
    path('reg/',views.reg_page,name='reg_page'),
    path('log/',views.log_page,name='log_page'),
    path('logot/',views.logout_page,name='logout_page'),
    path('like/<int:id>/', views.like_blog,name='like_blog'),
    path('comment/<int:id>/', views.blog_details,name='blog_details'),
]