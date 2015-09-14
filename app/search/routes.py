
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
    """
    This is the main search code. Uses BeautifulSoup to scrape
    the YCombinators front page for links and searches one-level
    deep for the query string.
    """
    form = SearchForm()
    	
    result_list = []
    url_list = []
    
    if request.method == 'POST':

        def generate_url_list():
            """
            Generates a list of URLs scrapped from the YCombinator
            front page. 
            """
            r = requests.get('https://news.ycombinator.com/')
            soup = BeautifulSoup(r.content)
            target = soup.find_all('td', attrs={'class':'title'}) # selects all 'td' elements with class 'title'         
            # 'target' is a ResultSet object, which for some reason wouldn't
            # let me call methods over it again. Hence will have to 're-soup' it.
            stringtarget = unicode.join(u'\n', map(unicode, target)) 
            soupagain = BeautifulSoup(stringtarget)
            # Able to call the find_all() method now. Couldn't find 
            # an alternative(better?) approach to this.
            for link in soupagain.find_all('a'):
                url_dict = {
                        "url": link.get('href'),
                        "text": link.text
                }
                url_list.append(url_dict)

            return url_list # Dictionary of URLs from YCombinator


	for url in generate_url_list():    
            # Some internal links were also scraped which were breaking
            # the search. I added a check to 'get' the URL only if it has
            # an 'http' part, making it a full URL.
            if "http" in url['url']:
	        r = requests.get(url['url'])
	        soup = BeautifulSoup(r.content)
                q = form.queryfield.data
                # Taught myslef all I can about regex. Still a bit shaky. 
                # re.compile converts a regex into a regex object, while
                # performing a sort of search, with passed parameters.
                # This one worked for me.
                result = soup(text=re.compile(q, re.IGNORECASE))
                hits = len(result)
                # Only the results with more than 0 hits are added to the
                # result_list 
                if hits > 0:
	            result_dict = {
		        "url": url['url'],
		        "hits": hits,
                        "text": url['text']
	            }
	            result_list.append(result_dict)

        # The result_list is sorted in the descending order according to 'hits' key.
        # 'hits' corresoponds to the number of occurances of the search term in a page.
        sorted_result_list = sorted(result_list, key=itemgetter('hits'), reverse = True)

        return render_template('results.html',
				result_list = sorted_result_list,
                                url_list = generate_url_list(),
                                query = form.queryfield.data,
                                form = form)

    elif request.method == 'GET':
        return redirect(url_for('index'))



