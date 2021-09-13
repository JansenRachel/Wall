# from typing import Text
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField
import re
import bcrypt
from django.http import request
from django.shortcuts import redirect

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['firstname']) < 2:
            errors['first_name'] = "Your name must contain letters only and be at least 2 characters in length."
        
        if len(postData['lastname']) < 2:
            errors['last_name'] = "Your name must contain letters only and be at least 2 characters in length."
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_match'] = ("Invalid email address")
        
        email_check = self.filter(email=postData['email'])
        if email_check:
            errors['email_unique'] = "Email already exists"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        
        if postData['password'] != postData['confirmPw']:
            errors['password_match'] = "Check that your passwords match"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_match'] = ("Invalid email address")
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        return errors
        

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = UserManager()

class MessagePost(models.Model):
    poster = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    message = models.TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
class Comment(models.Model):
    comment_content = models.TextField()
    poster = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    message = models.ForeignKey(MessagePost, related_name= "comments", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)