from django.contrib.auth import login as authuser
from django.contrib.auth import logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.timezone import datetime as time

from questions.models import Question, Tag, Answer, Like
from questions.paginator import PaginatorClass
from .forms import LoginForm, SettingsForm, RegistrationForm


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

def testform(request):

    form = RegistrationForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            return HttpResponse("OK 200")
        else:
            notfield=""
            email = ""
            if '__all__' in form.errors: notfield = form.errors['__all__'][0]
            if 'email' in form.errors: email = form.errors['email'][0]
            error_set = {"notfield":notfield,"email":email}
            return render(request, 'questions/forms/testform.html', {'form': form,'errors': error_set})
    return render(request, 'questions/forms/testform.html', {'form':form})

def post_question(request):

    return HttpResponse(Question.objects.postQuestion(request))

def sign_out(request):
    if request.user.is_authenticated:
        if 'qfilter' in request.session:
            del request.session['qfilter']
        logout(request)
    return redirect('/')

def post_comment(request):

    if request.POST:
        post_id = str(request.POST['post_id_data']).split("/")[-2]
        question = Question.objects.all().filter(id=post_id)[0]
        author = request.user
        comment_text = request.POST['comment_text']

        comment = Answer(user=author,question=question,text=comment_text,created=time.now())
        comment.save()
    return HttpResponse(200)

def registration(request):

    form = RegistrationForm(request.POST or None, request.FILES or None)
    tags = Tag.objects.getPopularTags()
    if request.POST:
        if form.is_valid():
            form.register()
            user = authenticate(request,username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user:
                authuser(request, user)
                return HttpResponseRedirect("/")
        else:
            notfield = ""
            email = ""
            if '__all__' in form.errors: notfield = form.errors['__all__'][0]
            if 'email' in form.errors: email = form.errors['email'][0]
            error_set = {"notfield": notfield, "email": email}
            return render(request, 'questions/registration.html', {'form': form, 'errors': error_set,'tags':tags})
    return render(request, 'questions/registration.html', {'form': form,'tags':tags})

    # return render(request, 'questions/registration.html',{'tags':tags})

def login(request):
    form = LoginForm(request.POST or None)
    tags = Tag.objects.getPopularTags()

    if request.POST:
        if form.is_valid():
            usr = form.cleaned_data['login']
            pwd = form.cleaned_data['password']
            user = authenticate(username=usr, password=pwd)
            if user:
                authuser(request, user)
                return HttpResponseRedirect("/")
            else:
                errors = {'user':'Пользователь не найден.'}
                return render(request, 'questions/login.html', {'tags': tags, 'form': form,'errors':errors})

    return render(request,'questions/login.html',{'tags':tags,'form':form})

def settings(request):
    if request.user.is_authenticated:
        form = SettingsForm(request.POST or None)
        tags = Tag.objects.getPopularTags()
        user = request.user

        if not request.POST:
            form.initial = {'login':user.username, 'email':user.email,'nickname':user.profile.nickname}

        if request.POST:
            if form.is_valid():
                print("YAY!")
                form.save_settings(request.user,form.cleaned_data)
                info = {'save':'Настройки успешно сохранены.'}
                return render(request, 'questions/settings.html', {'tags': tags, 'user': user, 'form': form,'info':info})
            else:
                errors = {'login': '', 'email': '', 'nickname': ''}

                if 'login' in form.errors:
                    errors['login'] = form.errors['login'][0]
                if 'email' in form.errors:
                    errors['email'] = form.errors['email'][0]
                if 'nickname' in form.errors:
                    errors['nickname'] = form.errors['nickname'][0]
                return render(request, 'questions/settings.html', {'tags': tags, 'user': user, 'form': form,'errors':errors})

    return render(request, 'questions/settings.html', {'tags': tags, 'user': user,'form':form})

def likedislike(request):

    if request.POST:
        like = Like(author=request.user,
                    question=Question.objects.get(pk=request.POST['post_id']),
                    like_type=request.POST['action'])
        like.save()
        q = Question.objects.get(pk=request.POST['post_id'])
        q.rating +=int(request.POST['action'])
        author = q.user.profile
        author.rating +=int(request.POST['action'])
        author.save()
        print(q.rating)
        q.save()

    return HttpResponse(q.rating)

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
