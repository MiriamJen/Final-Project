from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages 

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for error in errors.values():
            messages.error(request, error)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, "Invalid Email/Password")
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect ('/success')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        return redirect('/success')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'reviews': Review.objects.all(),
    }
    return render(request, 'success.html', context)

def post_review(request):
    Review.objects.create(title=request.POST['title'], rose=request.POST['rose'], bud=request.POST['bud'], thorn=request.POST['thorn'], review_type=request.POST['review_type'], reviewer=User.objects.get(id=request.session['user_id']))
    return redirect('/success')

def about_us(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'reviews': Review.objects.all(),
        }
        return render(request, 'about_us.html', context)
    else:
        return render(request, 'about_us.html')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['user_id'])
    review = Review.objects.get(id=id)
    request.session['review_id'] = review.id
    Comment.objects.create(comment=request.POST['comment'], poster=poster, review_comment=review)
    return redirect(f'/review_page/{id}')

def review_page(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'review': Review.objects.get(id=id)
    }
    return render(request, 'review_page.html', context)

def review_types(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'reviews':Review.objects.all(),
    }
    return render(request, 'review_types.html', context)

def profile(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def add_like(request, id):
    liked_review = Review.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_review.user_likes.add(user_liking)
    return redirect('/success')

def delete_comment(request, id):
    to_delete = Comment.objects.get(id=id)
    to_delete.delete()
    review_id = request.session['review_id']
    return redirect(f'/review_page/{review_id}')

def delete_review(request, id):
    user = User.objects.get(id=request.session['user_id'])
    to_delete = Review.objects.get(id=id)
    to_delete.delete()
    return redirect(f'/user_profile/{user.id}')

def edit(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user,
        'reviews': Review.objects.all(),
    }
    return render(request, "edit.html", context)

def update(request, id):
    to_edit = User.objects.get(id=id)
    to_edit.first_name = request.POST['first_name']
    to_edit.last_name = request.POST['last_name']
    to_edit.email = request.POST['email']
    to_edit.username = request.POST['username']
    to_edit.save()
    request.session['user_name'] = f"{to_edit.first_name} {to_edit.last_name}"
    return redirect(f'/user_profile/{to_edit.id}')
# Create your views here.
