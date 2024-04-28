"""
URL configuration for scoutsales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.http import HttpResponseRedirect
from django.urls import path, reverse

from . import views

urlpatterns = [
    path('', lambda request: HttpResponseRedirect(reverse('items-create')), name='home'),
    path('index.html', lambda request: HttpResponseRedirect(reverse('items-create'))),
    path('items', views.create, name="items-create"),
    path('items/all', views.items, name="items-all"),
    path('items/<slug:slug>', views.item, name="items"),
    path('items/<slug:slug>/print', views.print_item, name="items-print"),
    path('transactions', views.transactions, name="transactions"),
    path('transactions/active', views.basket, name="basket"),
    path('transactions/active/notes', views.basket_notes, name="basket-notes"),
    path('transactions/active/add', views.basket_add, name="basket-add"),
    path('transactions/active/sell', views.basket_sell, name="basket-sell"),
    path('transactions/active/clear', views.basket_clear, name="basket-clear"),
    path('transaction/<int:id>', views.transaction_view, name="transaction"),
]
