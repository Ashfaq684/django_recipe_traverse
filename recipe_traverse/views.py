from django.shortcuts import render
from recipes.models import Recipe
from django.core.paginator import Paginator

def home(request):
    recipes = Recipe.objects.all()
    
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    
    return render(request, 'index.html', {'recipes' : recipes})