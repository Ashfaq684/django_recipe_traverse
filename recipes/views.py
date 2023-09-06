from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import RecipeForm, RecipeSearchForm
from .models import Recipe, Category

# Create your views here.

def submit_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to create a new recipe
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user 
            new_recipe.save()
            return redirect('home')
    else:
        form = RecipeForm()
    
    return render(request, 'recipe_submission.html', {'form': form})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def recipe_list(request):
    # Get the selected category from the request's GET parameters
    selected_category = request.GET.get('category')

    # Retrieve all categories
    categories = Category.objects.all()

    if selected_category:
        # Filter recipes by the selected category
        recipes = Recipe.objects.filter(category__name=selected_category)
    else:
        # If "All" or no category is selected, retrieve all recipes
        recipes = Recipe.objects.all()
    
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    context = {
        'categories': categories,
        'recipes': recipes,
        'selected_category': selected_category,
    }

    return render(request, 'recipe_list.html', context)

def recipe_search(request):
    form = RecipeSearchForm()
    recipes = []

    if request.method == 'POST':
        form = RecipeSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            recipes = Recipe.objects.filter(Q(ingredients__icontains=search_query))
            
    return render(request, 'recipe_search.html', {'form': form, 'recipes': recipes})

def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Ensure that only the author can edit the recipe
    if recipe.author != request.user:
        return redirect('recipe_detail', recipe_id=recipe.id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipe_edit.html', {'form': form, 'recipe': recipe})