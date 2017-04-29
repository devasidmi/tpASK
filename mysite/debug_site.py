import questions.models
from .models import Tag

data = Tag.objects.all()
print(data)
