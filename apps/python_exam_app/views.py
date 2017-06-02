# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    context = {
    "user" : User.objects.all()
    }
    return render(request, 'python_exam_app/index.html', context)

def register(request):
    postData = {
        "first_name" : request.POST['first_name'],
        "alias" : request.POST['alias'],
        "email" : request.POST['email'],
        "password" : request.POST['password'],
        "conpass" : request.POST['conpass'],
        "dob" : request.POST['dob'],
    }
    result = User.objects.register(postData)
    print result
    if result[0] == True:
        request.session['id'] = result[1].id
        request.session['name'] = result[1].first_name
        return redirect('/quotes')
    if len(result[1]) !=0:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/')

def login(request):
    postData = {
        "email" : request.POST['email'],
        "password" : request.POST['password'],
    }
    result = User.objects.login(postData)
    print result
    if len(result) != 0:
        for error in result:
            messages.error(request, error)
        return redirect('/')#redirect back to registration page.
    else:
        request.session['name'] = User.objects.get(email=postData['email']).first_name
        request.session['id'] = User.objects.get(email=postData['email']).id
        return redirect('/quotes')


def process(request):
    postData = {
        "quotedby" : request.POST['quotedby'],
        "message" : request.POST['message'],
        "first_name" : request.session['name'],
        "id" : request.session['id'],
    }
    result = Quote.objects.validate(postData)

    if result[0] == True:
        print result
        return redirect('/quotes')
    if len(result) !=0:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/quotes')

def quotes(request):
    allquotes = Quote.objects.all().order_by('-created_at')
    context = {
        "quote" : allquotes
    }
    return render(request, 'python_exam_app/quotes.html', context)

def favquote(request, id):
    print id
    return redirect('/quotes')



def user(request):
    allquotes = Quote.objects.filter(author_id=request.session['id']).order_by('-created_at')
    print allquotes
    context = {
        "quote" : allquotes
    }
    return render(request, 'python_exam_app/user.html', context)



def logout(request):
    request.session.clear()
    return redirect('/')
