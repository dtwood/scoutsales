import secrets

from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models


class Item(models.Model):
    seller_email = models.EmailField(max_length=100)
    seller_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, help_text="A brief name for your item, for example \"Electric kettle\"")
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    donation = models.PositiveSmallIntegerField(validators=[validators.MinValueValidator(30), validators.MaxValueValidator(100)], help_text="The percentage of the value of your item to donate to 11th/9th Cambridge Scout Group")
    slug = models.SlugField(primary_key=True)

    def save(self, *args, **kwargs):
        if self.slug != "":
            return super(Item, self).save(*args, **kwargs)

        for _ in range(0, 10):
            new_slug = secrets.token_hex(4)
            if not Item.objects.filter(slug=new_slug).exists():
                self.slug = new_slug
                return super(Item, self).save(*args, **kwargs)
            else:
                raise ValueError("Couldn't generate a unique code.")
