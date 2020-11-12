import base64
import binascii
import functools
import hashlib
import importlib
import warnings
from collections import OrderedDict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils.crypto import (
    constant_time_compare, get_random_string, pbkdf2,
)
from django.utils.encoding import force_bytes, force_text
from django.utils.module_loading import import_string
from django.utils.translation import gettext_noop as _

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
# from django.contrib.auth.views import reset_password




def confirmation(request, code):

    get_auth = authentication.objects.get(auth_code = code)
    get_auth.isCompleted = True
    get_auth.save()

    return redirect("login")


def send_password_reset_link(user_email, myCodeHash):
    # me == my email address
    # you == recipient's email address
    sender = "resett.passwoord@gmail.com"
    receiever = user_email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Password reset link"
    msg['From'] = sender
    msg['To'] = user_email

    # Create the body of the message (a plain-text and an HTML version).
    # Create the body of the message (a plain-text and an HTML version).
    text = "Password reset link for makeVideo.com\n"
    html = """\
    <html>
    <head>


    </head>

    <body style='background-color:#f2f2f2; padding: 10%'>
        <div style='text-align:center; padding:30px; background-color:#ffffff; border-radius:10px; border:solid 1px #cccccc'>
        <h1 style="margin: auto 10px;">MakeVideo.com</h1>
        <br>
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif; margin-top:10px; margin-bottom:0px; font-size:20px; background-color:#0465f6; color:#ffffff; padding:8px; border-radius:1px;">
            Password reset link
            </p>

        <br>        
        <p style="font-size:16px; line-height:30px; text-align:left; color:#303030; font-family: Verdana, Geneva, Tahoma, sans-serif; margin-top:10px;">
            Hi registered! <br>
            <br>
            We are glad to help you in resetting your passowrd. Kindly &nbsp;<a href="http://127.0.0.1:8000/change-password/{}">click here</a> to open the reset password form<br> 
            <br>
            We are waiting to serve you for making quality video according to your need at the most simplest and easy way.<br>
            <br>
            Thanks for your time, <br>
            Team <i>makeVideo.pk</i>
            <br>
        </p>
    
        
        </div>
    </body>
    </html>
    """.format(myCodeHash)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender, 'ResetPassword1234')
    mail.sendmail(sender, user_email, msg.as_string())
    mail.quit()


def send_html_email(user_name, user_email, myCodeHash):
    # me == my email address
    # you == recipient's email address
    sender = "resett.passwoord@gmail.com"
    receiever = user_email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Authentication Email"
    msg['From'] = sender
    msg['To'] = user_email

    # Create the body of the message (a plain-text and an HTML version).
    # Create the body of the message (a plain-text and an HTML version).
    text = "Thanks for register on makeVideo.com\n"
    html = """\
    <html>
    <head>


    </head>

    <body style='background-color:#f2f2f2; padding: 10%'>
        <div style='text-align:center; padding:30px; background-color:#ffffff; border-radius:10px; border:solid 1px #cccccc'>
        <h1 style="margin: auto 10px;">MakeVideo.com</h1>
        <br>
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif; margin-top:10px; margin-bottom:0px; font-size:20px; background-color:#0465f6; color:#ffffff; padding:8px; border-radius:1px;">
            Thanks for registration
            </p>

        <br>        
        <p style="font-size:16px; line-height:30px; text-align:left; color:#303030; font-family: Verdana, Geneva, Tahoma, sans-serif; margin-top:10px;">
            Hi {}! <br>
            <br>
            We are glad to receive your sign up request. For complete your registration &nbsp;<a href="http://127.0.0.1:8000/confirmation/{}">click here</a><br> 
            <br>
            We are waiting to serve you for making quality video according to your need at the most simplest and easy way.<br>
            <br>
            Thanks for your time, <br>
            Team <i>makeVideo.pk</i>
            <br>
        </p>
    
        
        </div>
    </body>
    </html>
    """.format(user_name, myCodeHash)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender, 'ResetPassword1234')
    mail.sendmail(sender, user_email, msg.as_string())
    mail.quit()


def add_user_fields(request):
    output = {}
    try:
        if request.method == "GET":
            thisCode = request.GET.get('code')
            object_data = request.GET.get('object_data')
            object_data = json.loads(object_data)

            for i in object_data:
                thisRow = object_data[i]
                print(thisRow[0], thisRow[1], thisCode)
                
                user_field = user_fields(
                    input_name = thisRow[0],
                    input_type = thisRow[1],
                    code = thisCode
                )

                user_field.save()

            output['status'] = True
            output['code'] = thisCode
    except:
        output['status'] = False
    return JsonResponse(output)


def secret_code():
    CHAR = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(0, 20):
        index = randint(0, len(CHAR)-1)
        code += CHAR[index]
    return code


def add_product(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        thumbnail = request.FILES.get("thumbnail")
        previewLink = request.POST.get("previewLink")
        price = request.POST.get("price")
        myCode = request.POST.get("myCode")

        new_product = product(
            title = title,
            description = description,
            thumbnail = thumbnail,
            previewLink = previewLink,
            price = price,
            code = myCode
        )

        new_product.save()

        messages.info(request, "Your product has been added successfully along with the input fields!")

    return redirect("admin-panel")


def show_product(request, id):
    context = {}
    try:
        target_product = product.objects.get(id = id)
        context['product'] = target_product

        inputs = user_fields.objects.filter(code = target_product.code)

        context['inputs'] = inputs

    except:
        return redirect("index")

    return render(request, "product.html", context)


def admin_panel(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, "admin-panel.html")
    else:
        return redirect("index")

# main page function

def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        check_auth = authentication.objects.get(which_user = request.user)

        if not check_auth.isCompleted:
            return redirect("send-code")

    all_products = product.objects.all().order_by('-id')
    print(all_products)
    context = {
        'products': all_products
    }

    return render(request, 'main-page.html', context)

# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email'].lower()
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()

            new_authentication = authentication(which_user = user, auth_code = generate_code())
            new_authentication.save()

            send_html_email(user.first_name, user.username, new_authentication.auth_code)

            messages.info(request, "We have sent you a confirmation email. Kindly check it!")
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


def generate_code():    
    CHAR = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(0, 150):
        index = randint(0, len(CHAR)-1)
        code += CHAR[index]
    return code

def sendAgain(request):
    return render(request, "send-again.html")

def send_code_again(request):

    get_auth = authentication.objects.get(which_user = request.user)
    get_auth.auth_code = generate_code()

    send_html_email(request.user.first_name, request.user.username, get_auth.auth_code)

    get_auth.save()

    messages.info(request, "We have sent you confirmation email again. Kindly check it")

    return render(request, "send-again.html")

# login validation
def login_validation(request):
    output = {}
    if request.method == "GET" and request.is_ajax():
        email = request.GET['email'].lower()
        password = request.GET['password']

        user = auth.authenticate(username=email, password=password)
        if user is not None:
            output['stauts'] = True
            output['msg'] = "Login successfull!"
        else:
            output['status'] = False
            output['msg'] = "Incorrect login details!"

        return JsonResponse(output)

# function for login
def login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            
            check_auth = authentication.objects.get(which_user = request.user)

            if check_auth.isCompleted:
                return redirect("index")
            else:
                return redirect("send-code")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


def reset_password(request):
    context = {}
    if request.method == "POST":
        email = request.POST['email'].lower()
        print("email =>", email)

        if User.objects.filter(username = email).exists():
            that_user = User.objects.get(username = email)
    
            new_code = generate_code()

            if password_resetting.objects.filter(which_user = that_user).exists():
                focused_resetting = password_resetting.objects.get(which_user = that_user)
                focused_resetting.reset_code = new_code
                focused_resetting.save()
            else:
                new_resetting = password_resetting(
                    which_user = that_user,
                    reset_code = new_code
                )

                new_resetting.save()

            send_password_reset_link(email, new_code)

            context['message'] = "Password reset link has been sent to your email!"
        else:
            context['message'] = "Entered email is not associated with any account!"


    return render(request, "reset.html", context)

def change_password(request, code):
    print(code)
    context = {}
    if request.method == "POST":
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        

        context['pass1'] = pass1
        context['pass2'] = pass2
    

        if pass1 == pass2:
            focused_code_user = password_resetting.objects.get(reset_code = code)
            myFocusedUser = focused_code_user.which_user
            myFocusedUser.set_password(pass1)
            myFocusedUser.save()
            messages.info(request, "Your password has been changed successfully!")
            return redirect("login")
        else:
            messages.info(request, "Entered passwords don't match!")

    return render(request, "change-password.html", context)


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")

