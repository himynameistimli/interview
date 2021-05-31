import csv
import io

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView
from website import models as website_models
from website import forms as website_forms


class HomeView(TemplateView):
    template_name = 'website/home.html'
