from requests.api import post
from craig_app.models import Search
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
# to turn raw search strings into URL format
from requests.compat import quote_plus

from . import models


BASE_CRAIGSLIST_URL = 'https://miami.craigslist.org/search?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    # using python dictionary get to extract key from request dictionary
    text = request.POST.get('search')
    models.Search.objects.create(search_text=text)

    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(text))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(
                class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append(
            (post_title, post_url, post_price, post_image_url))

    context_dict = {
        'search': text,
        'final_postings': final_postings
    }
    return render(request, 'craig_app/new_search.html', context_dict)
