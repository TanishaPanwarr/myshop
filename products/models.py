from django.db import models
from django.urls import reverse

# Category Model
class Category(models.Model):
    title = models.CharField(max_length=300)
    primaryCategory = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

#Product Model
class  Product(models.Model):
    mainimage = models.ImageField(upload_to='products/', blank=True)
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000, verbose_name='Detail Text')
    price = models.FloatField()
    

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("mainapp:product", kwargs={
            'slug': self.slug
        })
     
class Article(models.Model):
    nid = models.IntegerField(default=0)
    headimage =models.ImageField(upload_to='pics', blank=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True)
    body = models.TextField()
    teaser = models.TextField('teaser', blank=True)
    created=models.DateField(auto_now=False, auto_now_add=False)
    pub_date=models.DateField(auto_now=False, auto_now_add=False)
    categories = models.ManyToManyField(Product)
    def __str__(self):
        return str(self.nid)