from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Question,Answer,Tag

def getPopularTags():
    tags = Tag.objects.all()
    return sorted(tags,key=lambda tag:tag.used, reverse=True)[0:3]

def getComments(id):
    answers = Answer.objects.all().filter(question_id = id)
    return answers

def get_q_id(request,id):
    post = Question.objects.all().filter(id="%s" % (id))[0]
    response = "TITLE: %s\n TEXT: %s\n CREATED: %s\n TAGS: %s" % (post.title, post.text, post.created, post.tags.name)
    print(response)
    comments = getComments(id)
    tags = getPopularTags()
    return render(request,'questions/post_page.html',{'post':post,'comments':comments,'tags':tags})

def questions_list(request):
    questions = Question.objects.newest()
    tags = getPopularTags()
    #assert False, questions
    return render(request, 'questions/questions_list.html', {'questions': questions,'tags':tags})
def registration(request):
    tags = getPopularTags()
    return render(request, 'questions/registration.html',{'tags':tags})
def login(request):
    tags = getPopularTags()
    return render(request,'questions/login.html',{'tags':tags})
def settings(request):
    tags = getPopularTags()
    return render(request,'questions/settings.html',{'tags':tags})
def logged(request):
    return render(request,'questions/logged_in.html',{})
def ask(request):
    tags = getPopularTags()
    return render(request,'questions/ask.html',{'tags':tags})
def simpleapp(request):
    resp = ['<p>Methods page</p>']
    print(request)
    print(request.GET)
    if request.method == 'GET':
        if (len(request.GET)):
            resp.append("GET<br>")
            print(request.GET.items)
            for item in request.GET:
                print (item, request.GET[item])
                arr = (item, '=', request.GET[item], '<br>')
                resp.append(''.join(arr))

    if request.method == 'POST':
        print(request.POST.items)
        resp.append("POST<br>")
        if (len(request.POST)):
            for item in request.POST:
                print (item, request.body)
                arr = (item, '=', request.POST[item], '<br>')
                resp.append(''.join(arr))
    return HttpResponse(resp)
