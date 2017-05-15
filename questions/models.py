from django.db import models
from django.shortcuts import render
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import datetime as time

from .paginator import PaginatorClass


class QuestionManager(models.Manager):

    def newest(self):
        return self.order_by('-id')

    def hot(self):
        return self.order_by('-rating')

    def tag(self, tag_name):
        tg = Tag.objects.get(name = tag_name)
        return tg.question_set.all()

    def comments(self, id):
        comments = Answer.objects.all().filter(question_id = id)
        return comments

    def postQuestion(self,request):
        post_tags = str(request.POST['tags']).split(" ")
        title = request.POST['title']
        text = request.POST['text']
        user = request.user
        tags = Tag.objects.all()

        if tags.count() > 0:
            last_tag_id = tags[tags.count() - 1].id
        else:
            last_tag_id = 0
        if Question.objects.all().count() > 0:
            last_question_id = Question.objects.all()[Question.objects.all().count() - 1].id
        else:
            last_question_id = 0
        question = Question()
        question.id = last_question_id + 1;
        question.created = time.now()
        question.title = title
        question.text = text
        question.user = user
        question.save()

        for tag in post_tags:
            if tag != "":
                if Tag.objects.all().filter(name=tag).count() == 0:
                    new_tag = Tag(name=tag)
                    new_tag.id = last_tag_id + 1
                    last_tag_id += 1
                    new_tag.used = 1
                    new_tag.save()
                    question.tags.add(last_tag_id)
                else:
                    tag = Tag.objects.all().filter(name=tag)[0]
                    tag.used += 1
                    tag.save()
                    question.tags.add(Tag.objects.all().filter(name=tag)[0].id)
        return 200

    def getQuestionsByTag(self,request,tag):
        tags = Tag.objects.getPopularTags()
        questions = Tag.objects.getPostsWithTag(tag)
        page = request.GET.get('page')
        return render(request, 'questions/questions_list.html', {'questions': questions,'paginator':PaginatorClass.paginate(questions,page),'tags':tags,'search_tag':tag})

    def getQuestionWithComments(self,request,id):
        post = Question.objects.all().filter(id="%s" % (id))[0]
        comments_list =  Question.objects.comments(id)
        page = request.GET.get('page')
        tags = Tag.objects.getPopularTags()
        return render(request,'questions/post_page.html',{'post':post,'paginator':PaginatorClass.paginate(comments_list,page),'tags':tags})

class TagManager(models.Manager):

    def getPopularTags(self):
        tags = Tag.objects.all()
        return sorted(tags,key=lambda tag:tag.used, reverse=True)[0:3]

    def getPostsWithTag(self,tag):
        return Tag.objects.get(name=tag).question_set.all()

class Tag(models.Model):
    class Meta:
        db_table = "tags"
    name = models.CharField(max_length = 20, unique = True)
    used = models.IntegerField(default=0)

    objects=TagManager()

    def __str__(self):
        return self.name

class Question(models.Model):
    class Meta:
        db_table = "questions"
    user = models.ForeignKey(User)
    title = models.CharField(max_length = 255)
    text = models.TextField()
    rating = models.IntegerField(default = 0, db_index=True)
    created = models.DateTimeField(default = datetime.datetime.now)
    tags = models.ManyToManyField(Tag)

    objects=QuestionManager()

    def __str__(self):
        return self.title

class Answer(models.Model):
    class Meta:
        db_table = "answers"
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    text = models.TextField()
    created = models.DateTimeField(default = datetime.datetime.now)
    #correct = models.BooleanField(default = False)

    def __str__(self):
        return self.text

class Profile(User):
    class Meta:
        db_table = "profiles"
    avatar = models.ImageField(blank=True,null=True)
    nickname = models.CharField(max_length = 20, default='')
    rating = models.IntegerField(default = 0)

    def __str__(self):
        return self.nickname

class Like(models.Model):
    class Meta:
        db_table = "likes"
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    like_type = models.IntegerField(default=0)
