from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, postData):
        errors = []
        if len(postData['first_name']) < 2:
            errors.append('First Name too short')
        if len(postData['alias']) < 2:
            errors.append('Alias too short')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Not a valid Email')
        if len(User.objects.filter(email=postData['email'])):
            errors.append('Email already exist')
        if len(postData['password']) < 8:
            errors.append('Password too short')
        if postData['password'] != postData['conpass']:
            errors.append('Password does not match')
        if len(errors) == 0:
            hashed_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
            newuser = User.objects.create(first_name=postData['first_name'], alias=postData['alias'], email=postData['email'], password=hashed_pw, dob=postData['dob'])
            return(True, newuser)
        else:
            return(False, errors)

    def login(self, postData):
        errors = []

        if User.objects.filter(email=postData['email']):
            form_pw = postData['password'].encode()
            db_pw = User.objects.get(email=postData['email']).password.encode()
            if not bcrypt.checkpw(form_pw, db_pw):
                errors.append('Incorrect password')
        else:
            errors.append('Email has not been registered')
        return errors


class QuoteManager(models.Manager):
    def validate(self, postData):
        errors = []
        if len(postData['quotedby']) < 3:
            errors.append('Quoted by needs to be more that 3 characters')
        if len(postData['message']) < 10:
            errors.append('Message needs to be more that 10 characters')
        if len(errors) == 0:
            newquote = Quote.objects.create(content=postData['message'], quote_author=postData['quotedby'], author=User.objects.get(first_name=postData['first_name']))
            return(True, newquote)
        else:
            return(False, errors)



class User(models.Model):
    first_name = models.CharField(max_length=38)
    alias = models.CharField(max_length=38)
    email = models.CharField(max_length=38)
    password = models.CharField(max_length=38)
    dob = models.DateField(auto_now=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __unicode__(self):
        return "id:" + str(self.id) + "first name" + self.first_name + "alias" + self.alias + "email" + self.email + "password" +  self.password + "dob" + self.dob

class Quote(models.Model):
    content = models.CharField(max_length=100)
    quote_author = models.CharField(max_length=38, null=True)
    author = models.ForeignKey(User)
    favq = models.ManyToManyField(User, related_name="favquotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __unicode__(self):
        return "id:" + str(self.id) + "content" + self.content
