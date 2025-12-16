from django.urls import path
from .views import (
    teacher_delete,
    logout_view,
    login_view, 
    teacher_directory, 
    filter_teachers, 
    import_teachers,
    teacher_detail,
    teacher_create,
    teacher_update
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', teacher_directory, name='teachers'),
    path('filter/', filter_teachers, name='filter'),
    path('import/', import_teachers, name='import_teachers'),
    path('logout/', logout_view, name='logout'),
    path('teacher/add/', teacher_create, name='teacher_create'),
    path('teacher/<int:pk>/', teacher_detail, name='teacher_detail'),
    path('teacher/<int:pk>/edit/', teacher_update, name='teacher_update'),
    path('teacher/<int:pk>/delete/', teacher_delete, name='teacher_delete'),
]
