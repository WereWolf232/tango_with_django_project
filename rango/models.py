from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(unique=True, max_length=128)
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField(blank=True, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
        
        
    # Added the below so it says "Categories" instead of "Categorys"
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name



class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

   

