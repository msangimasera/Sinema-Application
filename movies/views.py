from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Sinema',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)


def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://cdn.pixabay.com/photo/2017/02/26/03/59/frame-2099462__340.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.insert(data)
            messages.success(request,'{} successfully added'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request,'Error creating movie: {}'.format(e))
    return redirect('/')


def edit(request, movie_id):
    if request.method == 'POST':
        picurl = request.POST.get('url') or 'https://cdn.pixabay.com/photo/2017/02/26/03/59/frame-2099462__340.jpg';
        data = {
            'Name': request.POST.get('name'),
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes'),
            'Pictures': [{'url':picurl}]
        }
        try:
            response = AT.update(movie_id, data)
            messages.success(request,'{} successfully updated'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request,'Error updating movie: {}'.format(e))

    return redirect('/')

def delete(request, movie_id):
    movie_name = AT.get(movie_id)['fields'].get('Name')
    try:
        AT.delete(movie_id)
        messages.warning(request,'Ooops! You have deleted movie {}'.format(movie_name))
    except Exception as e:
        messages.warning(request,'Error deleting movie: {}'.format(e))

    return redirect('/')
