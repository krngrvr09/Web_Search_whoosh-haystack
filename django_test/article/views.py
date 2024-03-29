from django.shortcuts import render

from django.http import HttpResponse
from article.models import Article, Comment
from django.shortcuts import render_to_response
from forms import ArticleForm, CommentForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone
from haystack.query import SearchQuerySet
# Create your views here.


def articles(request):
	language = 'en'
	session_leanguage = 'en'

	if 'lang' in request.COOKIES:
		language = request.COOKIES['lang']
	args={}
	args.update(csrf(request))

	args['articles']=Article.objects.all()
	args['language']=language

	return render_to_response('articles.html',args)

def article(request, article_id=1):
	return render_to_response('article.html', {'article': Article.objects.get(id=article_id)})

def language(request, language='en'):
	response=HttpResponse("setting language to %s"%language)

	response.set_cookie('lang', language)
	return response

def create(request):
	if request.POST:
		form=ArticleForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/articles/all')
	else:
		form=ArticleForm()
	args={}
	args.update(csrf(request))

	args['form']=form
	
	return render_to_response('create_article.html', args)

def like_article(request, article_id):
	if article_id:
		a=Article.objects.get(id=article_id)
		count=a.likes
		count+=1
		a.likes=count
		a.save()
	return HttpResponseRedirect('/articles/get/%s'%article_id)

def add_comment(request, article_id):
	a=Article.objects.get(id=article_id)
	
	if request.method == "POST":
		f=CommentForm(request.POST)
		if f.is_valid():
			c=f.save(commit=False)
			c.pub_date=timezone.now()
			c.article = a
			c.save()
			return HttpResponseRedirect("/articles/get/%s"%article_id)

	else:
		f=CommentForm()

	args={}
	args.update(csrf(request))

	args['article']=a
	args['form']=f
	
	return render_to_response('add_comment.html', args)

def search_titles(request):
#	if request.method =="POST":
#		search_text = request.POST['search_text']
#	else:
#		search_text=''
#
#	articles = Article.objects.filter(title__contains=search_text)

	articles=SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text',''))
	return render_to_response('ajax_search.html', {'articles': articles})
