from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime

from products import models
# Create your views here.
def index(request):
    products = models.Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/index.html', context)

@login_required(login_url='/accounts/signup')
def create(request):
    if request.method == 'POST':
        product = models.Product()
        product.title = request.POST['title']
        product.pub_date = datetime.now()
        product.body = request.POST['body']
        product.url = request.POST['url']
        product.icon = request.FILES['product_icon']
        product.image = request.FILES['product_image']
        product.hunter = request.user
        product.save()
        return redirect('/products/'+ str(product.id))
    return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(models.Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'products/detail.html', context)

@login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(models.Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))