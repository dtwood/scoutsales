from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import SimpleTemplateResponse
from django.urls import reverse

from scoutsalesapp.forms import ItemForm
from scoutsalesapp.models import Item


def create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()

            return HttpResponseRedirect(reverse("items-created", kwargs={'slug': item.slug}))
    else:
        form = ItemForm()

    return render(request, "items/create.html", {"form": form})


def created(request, slug):
    item = Item.objects.get(slug=slug)
    return SimpleTemplateResponse('items/created.html', {"item": item})
