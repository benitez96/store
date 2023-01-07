from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    cost = models.FloatField()
    # stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def main_image(self):
        image = self.images.filter(is_main=True).first()
        if image:
            return image.image.url
        return None

    def __str__(self):
        return self.name

class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.image)

    class Meta:
        ordering = ['-is_main', 'pk']
    

class Sizes(models.Model):
    product = models.OneToOneField(Product, related_name='sizes', on_delete=models.CASCADE)
    xs = models.PositiveSmallIntegerField(default=0)
    s = models.PositiveSmallIntegerField(default=0)
    m = models.PositiveSmallIntegerField(default=0)
    l = models.PositiveSmallIntegerField(default=0)
    xl = models.PositiveSmallIntegerField(default=0)
    xxl = models.PositiveSmallIntegerField(default=0)
    xxxl = models.PositiveSmallIntegerField(default=0)

