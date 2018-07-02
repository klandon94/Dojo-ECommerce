from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-z]+$')

class CustomerManager(models.Manager):
    def register_validator(self, postdata):
        errors = {}

        if not postdata['first_name']:
            errors['first_name'] = 'Please enter your first name'
        elif len(postdata['first_name']) < 3:
            errors['first_name'] = 'Must be at least 3 characters'

        if not postdata['last_name']:
            errors['last_name'] = 'Please enter your last name'
        elif len(postdata['last_name']) < 3:
            errors['last_name'] = 'Must be at least 3 characters'

        if not postdata['reg_email']:
            errors['reg_email'] = 'Please enter a email'
        elif not EMAIL_REGEX.match(postdata['reg_email']):
            errors['reg_email'] = 'Invalid email address'

        if not postdata['reg_password']:
            errors['reg_password'] = 'Please enter a password'
        elif len(postdata['reg_password']) < 8:
            errors['reg_password'] = 'Password must be at least 8 characters'

        if not postdata['reg_confirm']:
            errors['reg_confirm'] = 'Please confirm your password'
        elif postdata['reg_confirm'] != postdata['reg_password']:
            errors['reg_confirm'] = 'Passwords do not match'
        
        return errors

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    isAdmin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomerManager()
    def __repr__(self):
        return "<Customer: {} {}>".format(self.first_name, self.last_name)