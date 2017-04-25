from django.db import models
from django.contrib.auth.models import User
import datetime

class QuestionManager(models.Manager):

    def newest(self):
        return self.order_by('-id')

    def hot(self):
        return self.order_by('-rating')

    def tag(self, tag_name):
        tg = Tag.objects.get(name = tag_name)
        return tg.question_set.all()


class Tag(models.Model):
    class Meta:
        db_table = "tags"
    name = models.CharField(max_length = 20, unique = True)
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
    avatar = models.ImageField()
    nickname = models.CharField(max_length = 20, default='')
    rating = models.IntegerField(default = 0)

class Like(models.Model):
    class Meta:
        db_table = "likes"
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    like_type = models.IntegerField(default=0)
