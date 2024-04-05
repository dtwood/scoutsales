from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from scoutsalesapp.forms import ItemForm
from scoutsalesapp.models import Item


def create(request):
    if request.method == "POST":
        if request.POST.get('skip_validation') is not None:
            form = ItemForm(initial=request.POST.items())
        else:
            form = ItemForm(request.POST)
            if form.is_valid():
                item = form.save()
                return HttpResponseRedirect(reverse("items-created", kwargs={'slug': item.slug}) + f"?token={item.owner_token}")
    else:
        form = ItemForm()

    return render(request, "items/create.html", {"form": form})


def item(request, slug):
    item = Item.objects.get(slug=slug)
    token = request.GET.get('token')

    if token is not None and token == item.owner_token:
        assert len(item.owner_token) == 8
        has_valid_token = True
    else:
        has_valid_token = False

    return render(request, 'items/item.html', {"item": item, "has_valid_token": has_valid_token})


def print_item(request, slug):
    item = Item.objects.get(slug=slug)
    return render(request, 'items/print.html', {"item": item})
