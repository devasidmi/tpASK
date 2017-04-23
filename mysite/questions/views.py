from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Question

def questions_list(request):
    questions = Question.objects.hot()
    #assert False, questions
    return render(request, 'questions/questions_list.html', {'questions': questions})
def registration(request):
	return render(request,'questions/registration.html',{})
def login(request):
	return render(request,'questions/login.html',{})
def settings(request):
	return render(request,'questions/settings.html',{})
def logged(request):
	return render(request,'questions/logged_in.html',{})
def ask(request):
	return render(request,'questions/ask.html',{})
def simpleapp(wsgi_request):
	resp = ['<p>Methods page</p>']
	print(wsgi_request)
	print(wsgi_request.GET)
	if wsgi_request.method == 'GET':
		if (len(wsgi_request.GET)):
			resp.append("GET<br>")
			print(wsgi_request.GET.items)
			for item in wsgi_request.GET:
				print (item, wsgi_request.GET[item])
				arr = (item, '=', wsgi_request.GET[item], '<br>')
				resp.append(''.join(arr))

	if wsgi_request.method == 'POST':
		print(wsgi_request.POST.items)
		resp.append("POST<br>")
		if (len(wsgi_request.POST)):
			for item in wsgi_request.POST:
				print (item, wsgi_request.body)
				arr = (item, '=', wsgi_request.POST[item], '<br>')
				resp.append(''.join(arr))
	return HttpResponse(resp)