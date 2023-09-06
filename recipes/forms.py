from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe  # Specify the model to use for the form
        fields = ['title', 'description', 'ingredients', 'instructions', 'image', 'category',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'w-full px-3 py-2 rounded-lg border '
                    ' text-gray-950 focus:outline-none '
                    ' focus:border-green-500'
                )
            })
    
class RecipeSearchForm(forms.Form):
    search_query = forms.CharField(label='Search by Ingredients', max_length=100)
