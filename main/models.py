from django.db import models
import re
from datetime import datetime, date

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        email_exists = User.objects.filter(email=(postData['email']))

        if email_exists:
            errors['email_exists'] = "Whoops, looks like that email is already being used! Try a different one."
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name needs to have at least 2 characters or more"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name needs to have at least 2 characters or more"
        if not email_check.match(postData['email']):
            errors['email'] = "Oops, invalid email address! Try again"
        if len(postData['password']) < 8:
            errors['password'] = "Password needs to be at least 8 character or more"
        if postData['password'] != postData['confirm_password']:
            errors['password_match'] = "Oops, passwords don't match! Try again"
        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "A title is required and must be 2 or more characters long"
        if len(postData['description']) < 5:
            errors['description'] = "Description must be at least 5 or more characters long"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # books_uploaded = []
    # books_liked = []

class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="books_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()