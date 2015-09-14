
from search import app
from flask import render_template, request, url_for, redirect, session
from forms import SearchForm
from models import db
from bs4 import BeautifulSoup
import requests, re
from operator import itemgetter

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    """
    The home page of the search engine. Has the search bar
    which accepts the query string. Redirects to the results
    page after the results are computed. WOW!
    """
    form = SearchForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('index.html', form=form)
        else:
            return redirect(url_for('search', q = form.queryfield.data))

    elif request.method == 'GET':
        return render_template('index.html', form=form)

@app.route('/search', methods = ['POST'])
def search():
    form = SearchForm()

    url_dump = ['http://masteringdjango.com/django-book/',
		'https://www.djangopackages.com/grids/g/blogs/',
		'https://code.djangoproject.com/wiki/Tutorials',
		'http://matthewdaly.co.uk/blog/2013/12/28/django-blog-tutorial-the-next-generation-part-1/',
		'http://www.creativebloq.com/netmag/get-started-django-7132932']
    	
    result_list = []
    url_list = []
    
    if request.method == 'POST':

        def generate_url_list():
            r = requests.get('https://news.ycombinator.com/')
            soup = BeautifulSoup(r.content)
            target = soup.find_all('td', attrs={'class':'title'})          
            stringtarget = unicode.join(u'\n', map(unicode, target))
            soupagain = BeautifulSoup(stringtarget)
            for link in soupagain.find_all('a'):
                url_dict = {
                        "url": link.get('href'),
                        "text": link.text
                }
                url_list.append(url_dict)

            return url_list


	for url in generate_url_list():    
            if "http" in url['url']:
	        r = requests.get(url['url'])
	        soup = BeautifulSoup(r.content)
                q = form.queryfield.data
                result = soup(text=re.compile(q, re.IGNORECASE))
                hits = len(result)
                if hits > 0:
	            result_dict = {
		        "url": url['url'],
		        "hits": hits,
                        "text": url['text']
	            }
	            result_list.append(result_dict)
        
        sorted_result_list = sorted(result_list, key=itemgetter('hits'), reverse = True)

        return render_template('results.html',
				result_list = sorted_result_list,
                                url_list = generate_url_list(),
                                query = form.queryfield.data,
                                form = form)

    elif request.method == 'GET':
        return redirect(url_for('index'))



