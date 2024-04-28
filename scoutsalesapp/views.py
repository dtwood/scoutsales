import datetime
import logging

from django.contrib.auth.decorators import permission_required
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from scoutsalesapp.forms import ItemForm
from scoutsalesapp.models import Item, Transaction


def create(request):
    if request.method == "POST":
        if request.POST.get('skip_validation') is not None:
            form = ItemForm(initial=request.POST.items())
        else:
            form = ItemForm(request.POST)
            if form.is_valid():
                item = form.save()
                return HttpResponseRedirect(reverse("items", kwargs={'slug': item.slug}) + f"?token={item.owner_token}")
    else:
        form = ItemForm()

    return render(request, "items/create.html", {"form": form})


def item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    token = request.GET.get('token')

    if token is not None and token == item.owner_token:
        assert len(item.owner_token) == 8
        has_valid_token = True
    else:
        has_valid_token = False

    sold = item.sold_in is not None

    return render(request, 'items/item.html', {"item": item, "has_valid_token": has_valid_token, "sold": sold})


def print_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    return render(request, 'items/print.html', {"item": item})


@permission_required("scoutsalesapp.add_transaction")
def basket(request):
    transaction = Transaction.objects.get_or_create(created_by=request.user, sold_at=None)[0]
    total = sum(i.price for i in transaction.item_set.all())

    return render(request, 'transaction/basket.html', {"transaction": transaction, "total": total})


@permission_required("scoutsalesapp.add_transaction")
def basket_notes(request):
    transaction = Transaction.objects.get_or_create(created_by=request.user, sold_at=None)[0]

    transaction.notes = request.POST['notes']
    transaction.save()

    return HttpResponseRedirect(reverse('basket'))



@permission_required("scoutsalesapp.add_transaction")
def basket_add(request):
    item = get_object_or_404(Item, slug=request.POST['slug'], sold_in=None)
    transaction = Transaction.objects.get_or_create(created_by=request.user, sold_at=None)[0]
    item.sold_in = transaction
    item.save()

    return HttpResponseRedirect(reverse('basket'))


@permission_required("scoutsalesapp.add_transaction")
def basket_sell(request):
    transaction = Transaction.objects.get_or_create(created_by=request.user, sold_at=None)[0]
    transaction.sold_at = datetime.datetime.now()
    transaction.save()

    return HttpResponseRedirect(reverse('transaction', kwargs={"id": transaction.id}))


@permission_required("scoutsalesapp.add_transaction")
def basket_clear(request):
    transaction = Transaction.objects.get_or_create(created_by=request.user, sold_at=None)[0]
    transaction.item_set.clear()
    transaction.save()

    return HttpResponseRedirect(reverse('basket'))


@permission_required("scoutsalesapp.view_transaction")
def transactions(request):
    transactions = Transaction.objects.all().annotate(Sum('item__price', default=0)).annotate(Count('item')).order_by("-id")
    total_price = sum(t.item__price__sum or 0 for t in transactions)
    total_count = sum(t.item__count for t in transactions)
    items = Item.objects.aggregate(Sum('price'), Count('slug'))
    progress = total_count / items['slug__count'] * 100
    return render(request, 'transaction/transactions.html', {"transactions": transactions, "items": items, "total_price": total_price, "total_count": total_count, "progress": progress})


@permission_required("scoutsalesapp.view_transaction")
def transaction_view(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    total = sum(i.price for i in transaction.item_set.all())
    return render(request, 'transaction/transaction.html', {"transaction": transaction, "total": total})
