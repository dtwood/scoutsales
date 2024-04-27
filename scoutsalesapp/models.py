import secrets

from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils.text import slugify


class Transaction(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    sold_at = models.DateTimeField(default=None, blank=True, null=True)


def token_hex_4():
    return secrets.token_hex(4)


class Item(models.Model):
    seller_email = models.EmailField(max_length=100)
    seller_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, help_text="A brief name for your item, for example \"Electric kettle\"")
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    donation = models.PositiveSmallIntegerField(default=40, validators=[validators.MinValueValidator(25),
                                                                        validators.MaxValueValidator(100)],
                                                help_text="The percentage of the value of your item (minimum 25%) to donate to 11th/9th Cambridge Scout Group")
    slug = models.SlugField(primary_key=True)
    owner_token = models.CharField(max_length=8, null=True, default=token_hex_4)
    sold_in = models.ForeignKey(Transaction, on_delete=models.PROTECT, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.slug != "":
            return super(Item, self).save(*args, **kwargs)

        initials = slugify(''.join(x[0] for x in self.seller_name.split(' ')).lower())
        if initials == '':
            raise ValueError("Couldn't generate a unique code.")
        for i in range(1, 100):
            new_slug = f"{initials}-{i:02}"
            if not Item.objects.filter(slug=new_slug).exists():
                self.slug = new_slug
                return super(Item, self).save(*args, **kwargs)
        else:
            raise ValueError("Couldn't generate a unique code.")
