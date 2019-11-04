from django.shortcuts import render
from django.contrib import messages
from airtable import Airtable
import os

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
             'Sinema',
             os.environ.get('AIRTABLE_API_KEY'))



# Create your views here.
def home_page(request):
    user_query = request.GET.get('query','')
    search_result = AT.get_all(formula="FIND('" +user_query.lower()+ "', LOWER({Name}))")
    stuff_for_frontend = {'search_result':search_result}
    return render(request, 'movies/movies_stuff.html',stuff_for_frontend)
