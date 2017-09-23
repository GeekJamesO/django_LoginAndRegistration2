# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt
import re


class UserManager(models.Manager):
    def Creator(self, RequestPost):
        newUser = self.create(
            UserName = RequestPost['UserName'],
            First_Name = RequestPost['First_Name'],
            Last_Name = RequestPost['Last_Name'],
            Email = RequestPost['Email'],
            Birthday = RequestPost['Birthday'],
            Password = bcrypt.hashpw(RequestPost['Password'].encode(), bcrypt.gensalt())
        )
        return newUser

    def LoginVal(self, RequestPost):
        results = {'status' : True, 'errors' : [], 'user' : None }
        # userName = RequestPost['UserName']
        # lookForUser = self.filter(UserName = userName)
        email = RequestPost['Email']
        Password = RequestPost['Password']

        users = self.filter(Email = email)
        if (len(users) < 1):
            results['errors'].append("The username does not exist.")
        else:
            goodPassword = bcrypt.checkpw(Password.encode(), users[0].Password.encode())
            if (goodPassword):
                results['user'] = users[0]
            else:
                results['errors'].append("The username and password do not match.")
        results['status'] = ( 0 == len(results['errors']) )
        return results

    def Validate(self, RequestPost):
        results = {'status' : True, 'errors' : [] }
        UserName = RequestPost['UserName']
        if (len(UserName) < 3):
            results['errors'].append("UserName '{}' is too short, you need atleast 3 characters".format(UserName) )
        # TODO: Is alpha?

        First_Name = RequestPost['First_Name']
        if (len(First_Name) < 3):
            results['errors'].append("First_Name '{}' is too short, you need atleast 3 characters".format(First_Name) )
        # TODO: Is alpha?

        Last_Name = RequestPost['Last_Name']
        if (len(Last_Name) < 3):
            results['errors'].append("Last_Name '{}' is too short, you need atleast 3 characters".format(Last_Name) )
        # TODO: Is alpha?

        email = RequestPost['Email']
        regexResult = re.search(r'\w+@\w+\.\w{3}',email)
        if not regexResult:
            results['errors'].append("Email '{}' format is not valid".format(email) )

        Birthday = RequestPost['Birthday']
        # TODO: Validate this..

        Password = RequestPost['Password']
        if (len(Password) < 8):
            results['errors'].append("Password '{}' is too short, you need atleast 8 characters".format(Password) )
        Confirm = RequestPost['Confirm']
        if (Password != Confirm):
            results['errors'].append("Password and confirm PW does not match.")

        print self.filter(Email=email)
        if 0 < len(self.filter(Email=email)):  #self == user.objects
            results['errors'].append("A user with '{}' already exists in the database".format(email) )

        #Done with validation
        results['status'] = 0 == len(results['errors'])
        print results['errors']

        return results

class User(models.Model):
    UserName = models.CharField(max_length = 200)
    First_Name = models.CharField(max_length = 200)
    Last_Name = models.CharField(max_length = 200)
    Email = models.CharField(max_length = 200)
    Birthday = models.CharField(max_length = 200)
    Password = models.CharField(max_length = 200)
    Confirm = models.CharField(max_length = 200)
    objects = UserManager()
