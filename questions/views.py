from django.contrib.auth import login as authuser
from django.contrib.auth import logout, authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.timezone import datetime as time


from questions.models import Question, Tag, Answer
from questions.paginator import PaginatorClass


def questions_list(request):
    if request.POST and 'qfilter' in request.POST:
        qfilter = request.POST['qfilter']
        if qfilter == 'new':
            questions = Question.objects.newest()
        if qfilter == 'trend':
            questions = Question.objects.hot()
        request.session['qfilter'] = qfilter
        return HttpResponse("reload")
    else:
        if 'qfilter' in request.session:
            qfilter = request.session['qfilter']
            if qfilter == 'new':
                questions = Question.objects.newest()
            if qfilter == 'trend':
                questions = Question.objects.hot()
        else:
            questions = Question.objects.newest()
    page = request.GET.get('page')
    tags = Tag.objects.getPopularTags()
    # assert False, questions
    return render(request, 'questions/questions_list.html', {'questions': questions,'tags':tags,'paginator':PaginatorClass.paginate(questions,page)})

def post_question(request):

    return HttpResponse(Question.objects.postQuestion(request))

def sign_out(request):
    if request.user.is_authenticated:
        del request.session['qfilter']
        logout(request)
    return redirect('/')

def sign_in(request):
    if request.POST:
        usr = request.POST['login']
        pwd = request.POST['password']
        user = authenticate(request,username=usr,password=pwd)
        if user:
            authuser(request,user)
    return HttpResponse(200)

def post_comment(request):

    if request.POST:
        post_id = str(request.POST['post_id_data']).split("/")[-2]
        question = Question.objects.all().filter(id=post_id)[0]
        author = request.user
        comment_text = request.POST['comment_text']

        comment = Answer(user=author,question=question,text=comment_text,created=time.now())
        comment.save()
    return HttpResponse(200)

def save_settings(request):
    if request.POST:
        user = request.user
        user.email = request.POST['email']
        user.username = request.POST['login']
        user.profile.nickname = request.POST['nickname']
        user.profile.save()
        user.save()
    return HttpResponse(200)

def registration(request):
    tags = Tag.objects.getPopularTags()
    return render(request, 'questions/registration.html',{'tags':tags})

def login(request):
    tags = Tag.objects.getPopularTags()
    return render(request,'questions/login.html',{'tags':tags})

def settings(request):
    if request.user.is_authenticated:
        tags = Tag.objects.getPopularTags()
        user = request.user
        return render(request, 'questions/settings.html', {'tags': tags, 'user': user})
    return redirect('/login')

def logged(request):
    return render(request,'questions/logged_in.html',{})

def ask(request):
    tags = Tag.objects.getPopularTags()
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
