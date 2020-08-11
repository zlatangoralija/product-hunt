from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, VoteUser
from django.utils import timezone

# Create your views here.

def home(request):
    products = Product.objects.all
    return render(request, 'products/home.html', {'products': products})

@login_required(login_url="/accounts/login/")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['image'] and request.FILES['icon']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']

            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'https://' + request.POST['url']

            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required'})
    else:
        return render(request, 'products/create.html')

@login_required(login_url="/accounts/login/")
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})

@login_required(login_url="/accounts/login/")
def upvote(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        productVote = VoteUser.objects.get(product_id=product.id, user_id=request.user.id)
    except VoteUser.DoesNotExist:
        productVote = None

    if productVote is None:
        product.votes_total += 1
        product.save()

        productVote = VoteUser()
        productVote.user_id = request.user.id
        productVote.product_id = product.id
        productVote.vote_date = timezone.datetime.now()
        productVote.save()
    else:
        messages.error(request, 'You already voted for this product!')
        return redirect('/products/' + str(product.id))

    return redirect('/products/' + str(product.id))
