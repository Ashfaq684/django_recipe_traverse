from django.urls import path
from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('submit-recipe/', views.submit_recipe, name='submit_recipe'),
    path('<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('categories/', views.recipe_list, name='categories'),
    path('recipe_search/', views.recipe_search, name='search'),
    path('<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
]