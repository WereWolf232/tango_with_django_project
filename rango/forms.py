from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text="Please enter the category name.")
    # deleted the likes, views, and slug because they're initialised in model
    # can't actually delete because of tests
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Category
        fields = ("name",)



class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Page
        exclude = ('category',)
        
    # overriden method
    def clean(self):
        cleaned_data = self.cleaned_data 
        url = cleaned_data.get('url')
        # If url is not empty and doesn't start with 'http://', # then prepend 'http://'.
        # this is absolutely retarded and doesn't work (because normal pages are https), but the tests require it
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
          
        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta: 
        model = User
        fields = ('username', 'email', 'password',)
            
            
class UserProfileForm(forms.ModelForm): 
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)