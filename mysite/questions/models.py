from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse
from django.db.models.functions import Coalesce
import datetime


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/static/photos')

class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(storage=fs)
    info = models.TextField(default='mm')

    def get_avatar(self):
        return '/uploads/'+ str(self.avatar)

class TagManager(models.Manager):
    def get_by_title(self, title):
        return self.get(title=title)


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def get_url(self):
        return reverse(kwargs={'tag': self.title})
    objects=TagManager()


class QuestionQuerySet(models.QuerySet):
    def with_tags(self):
        return self.prefetch_related('tags')

    def with_answers(self):
        res = self.prefetch_related('answer_set')
        return res

    def order_by_popularity(self):
        return self.order_by('-likes')

    def with_answers_count(self):
        return self.annotate(answers_count=Count('answer__id', distinct=True))

    def with_author(self):
        return self.select_related('owner').select_related('owner__user')



class QuestionManager(models.Manager):
    def get_queryset(self):
        qs = QuestionQuerySet(self.model, using=self._db)
        return qs.with_tags().with_answers_count().with_author()

    def list_new(self):
        return self.order_by('-date')

    def list_hot(self):
        return self.order_by('-likes')

    def list_tag(self, tag):
        return self.filter(tags=tag)

    def get_single(self, id_):
        res = self.get_queryset()
        return res.with_answers().get(id=id_)

    def get_best(self):
        week_ago = timezone.now() + datetime.timedelta(-7)
        return self.get_queryset().order_by_popularity().with_date_greater(week_ago)


class Question(models.Model):
    owner = models.ForeignKey(Profile)
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    objects = QuestionManager()
    class Meta:
        ordering = ['-date']

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class LikeToQuestionManager(models.Manager):

    def has_question(self, question):
        return self.filter(question=question)

    def sum_for_question(self, question):
        res = self.has_question(question).aggregate(sum=Sum('value'))['sum']
        return res if res else 0

    def add_or_update(self, owner, question, value):
        obj, new = self.update_or_create(
                owner=owner,
                question=question,
                defaults={'value': value}
                )

        question.likes = self.sum_for_question(question)
        question.save()
        return new


class Answer(models.Model):
    owner = models.ForeignKey(Profile)
    question = models.ForeignKey(Question)
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)

class LikeToQuestion(models.Model):
    UP = 1
    DOWN = -1

    question = models.ForeignKey(Question)
    owner = models.ForeignKey(Profile)
    value = models.SmallIntegerField(default=1)
    objects = LikeToQuestionManager()

class LikeToAnswerManager(models.Manager):
    def has_answer(self, answer):
        return self.filter(answer=answer)

    def sum_for_answer(self, answer):
        res = self.has_answer(answer).aggregate(sum=Sum('value'))['sum']
        return res if res else 0

    def add_or_update(self, owner, answer, value):
        obj, new = self.update_or_create(
                owner=owner,
                answer=answer,
                defaults={'value': value}
                )

        answer.likes = self.sum_for_answer(answer)
        answer.save()
        return new

class LikeToAnswer(models.Model):
    UP = 1
    DOWN = -1

    answer = models.ForeignKey(Answer)
    owner = models.ForeignKey(Profile)
    value = models.SmallIntegerField(default=1)
    objects = LikeToAnswerManager()