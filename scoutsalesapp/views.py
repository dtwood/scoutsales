from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import SimpleTemplateResponse

from scoutsalesapp.forms import ItemForm
from scoutsalesapp.models import Item


def create(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ItemForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            item = form.save()

            return HttpResponseRedirect(f"/items/{item.slug}/created")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ItemForm()

    return render(request, "items/create.html", {"form": form})


def created(request, slug):
    item = Item.objects.get(slug=slug)
    return SimpleTemplateResponse('items/created.html', {"item": item})
