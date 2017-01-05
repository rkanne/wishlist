from __future__ import unicode_literals
from django.db import models
import datetime
import re
import bcrypt

PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$')

class RegistrationManager(models.Manager):
    def register(self, name, username, password, confirm_password, date_hired):
        message = []
        if len(name) <3 and len(username) <3:
        	message.append("Your name and username should not contain fewer than 3 characters!!")
        	if len(password) == 0:
        		message.append("Password is required")
        elif not PASSWORD_REGEX.match(password):
            message.append("Password is not VALID!!")
            message.append("Password should contain at least 1 Uppercase Alphabet, 1 Lowercase Alphabet and 1 Number")
        if len(password) < 1:
        	message.append("Password cannot be blank!")
        if len(confirm_password) < 1:
        	message.append("Confirm Password cannot be blank!")
        if password != confirm_password:
        	message.append("Passwords do not match.")
        if len(date_hired) < 1:
            message.append("Date hired cannot be blank!")
        if len(message) != 0:
            return (False, message)
        else:
        	pw_hash = bcrypt.hashpw(str(password), bcrypt.gensalt())
        	registration = Users.registerMgr.create(name=name,username=username, password=pw_hash, date_hired=date_hired)
        	registration.save()
        return (True, registration)

class LoginManager(models.Manager):
    def login(self, username, password):
        login_message = []
        if  len(username) <1 and len(password) < 1:
            login_message.append("Username and Password cannot be blank!")
        if len(username) == 0:
            login_message.append("Username is required")
            if len(password) == 0:
                login_message.append("Password is required")
        elif not PASSWORD_REGEX.match(password):
            login_message.append("Password is not VALID!!")
        if len(login_message) != 0:
            return (False, login_message)
        else:
        	print "False======"
        	login = Users.loginMgr.filter(username=username)
        	if len(login) < 1:
        		login_message.append("User does not exist in database")
        	elif (bcrypt.checkpw(str(password),str(login[0].password))):
        		return(True, login[0])
        	else:
        		login_message.append("Password is incorrect please try again")
                return (False, login_message)

class WishListsManager(models.Manager):
    def add(self, item_name):
        
        wish_message = []
        if len(item_name) < 3:
            wish_message.append('Item/Product must be more than 3 characters')

        if len(wish_message) != 0:
            return (False, wish_message)
        else:
            wish_message.append("*** You have added your Item!!! ***")
            return (True, wish_message)

class JoinsManager(models.Manager):
    def join(self):
            return (True, "true")

class Users(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_hired = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    registerMgr = RegistrationManager()
    loginMgr = LoginManager()
    joinsMgr = JoinsManager()

class Wishlist(models.Model):
    item_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users)
    wishlistMgr = WishListsManager()

class Join(models.Model):
    wishlist = models.ForeignKey(Wishlist)
    user = models.ForeignKey(Users)
    joinsMgr = JoinsManager()

# class Join(models.Model):
# 	user = models.ForeignKey(Users, models.DO_NOTHING, related_name="owner")
# 	trip = models.ForeignKey(Trips, models.DO_NOTHING, related_name="join")
# 	created_at = models.DateTimeField(auto_now_add = True)
# 	updated_at = models.DateTimeField(auto_now = True)
# 	joinsMgr = JoinsManager()





