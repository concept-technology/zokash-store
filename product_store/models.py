from django.db import models

# Create your models here.
class Categories(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.title}'
    
class ProductsItem(models.Model):
    title = models.CharField(max_length=255)
    description= models.TextField(max_length=1000)
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    img_1  = models.ImageField(upload_to='static/media/img', default='img')
    img_2  = models.ImageField(upload_to='static/media/img', default='img')
    img_3  = models.ImageField(upload_to='static/media/img', default='img')
    img_4  = models.ImageField(upload_to='static/media/img', default='img')
    label = models.CharField( max_length=255, default='', blank=True)
    category = models.ForeignKey(Categories, default='', on_delete=models.CASCADE)
    slug = models.SlugField( default=title)
    gender= models.CharField(max_length=10, choices=(('male', 'male'), ('female', 'female')), default='female')
    display_on_home_page =models.BooleanField(default=False)
    is_banner =models.BooleanField(default=False)
    is_best_selling = models.BooleanField(default=False)
