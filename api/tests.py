from django.test import TestCase

# Create your tests here.

#Testear de las vistas de API el login. 

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Bucketlist


    
