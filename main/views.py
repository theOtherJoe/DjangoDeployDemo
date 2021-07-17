from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt

def log_reg(request):
    return render(request, "login_reg.html")

def register(request):
    if request.method == 'POST':
        user_errors = User.objects.user_validator(request.POST)
        if len(user_errors) > 0:
            for key, value in user_errors.items():
                messages.error(request, value)
            return redirect('/')

        hashed_passwd = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user1 = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_passwd
        )
        request.session['current_user'] = user1.id
        return redirect('/books')

def login(request):
    if request.method == 'POST':
        list_of_users = User.objects.filter(email=request.POST['email'])
        if list_of_users:
            user_logged = list_of_users[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user_logged.password.encode()):
                request.session['current_user'] = user_logged.id
                return redirect('/books')
            else:
                messages.error(request, "Invalid username or password, try again")
                return redirect('/')
        messages.error(request, "Username does not exist")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def user_and_books(request):
    context = {
        'current_user': User.objects.get(id=request.session['current_user']),
        'all_books': Book.objects.all()
    }
    return render(request, "user_books.html", context)

def add_book(request):
    if 'current_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    if request.method == 'POST':
        user = User.objects.get(id=request.session['current_user'])
        book_errors = Book.objects.book_validator(request.POST)
        if len(book_errors) > 0:
            for key, value in book_errors.items():
                messages.error(request, value)
            return redirect('/books')
        book_created = Book.objects.create(title = request.POST['title'], description = request.POST['description'], uploaded_by = user)
        book_created.users_who_like.add(user)
        request.session['book_created'] = book_created
    	return redirect(f'/books/{book_created.id}')

def show_book(request, book_id):
    context = {
        'current_user': User.objects.get(id=request.session['current_user']),
        'book': Book.objects.get(id=book_id),
        'all_books': Book.objects.all(),
    }
    return render(request, "book.html", context)

def update_book(request, book_id):
    if "update" in request.POST:
        book_errors = Book.objects.book_validator(request.POST)
        if len(book_errors) > 0:
            for key, value in book_errors.items():
                messages.error(request, value)
            return redirect('/books')
        book_to_update = Book.objects.get(id=book_id)
        book_to_update.description = request.POST['description']
        book_to_update.title = request.POST['title']
        book_to_update.save()
        return redirect('/books')
    if "delete" in request.POST:
        book = Book.objects.get(id=book_id)
        book.delete()
        return redirect('/books')

def add_favorite(request, book_id):
    current_user = request.session['current_user']
    book_to_favorite = Book.objects.get(id=book_id)
    book_to_favorite.users_who_like.add(current_user)
    return redirect('/books')

def unfavorite(request, book_id):
    current_user = request.session['current_user']
    book_to_unfavorite = Book.objects.get(id=book_id)
    book_to_unfavorite.users_who_like.remove(current_user)
    return redirect('/books')
