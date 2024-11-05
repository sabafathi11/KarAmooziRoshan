from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Dataset(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    users_with_access = models.ManyToManyField(User, related_name='accessible_datasets', blank=True)

    def __str__(self):
        return self.title

    @property
    def labeled_texts(self):
        num = 0
        for text in self.texts.all():
            if text.labels:
                num += 1
        return num


class Text(models.Model):
    content = models.TextField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='texts')
    labels = models.ManyToManyField('Label', related_name='texts', blank=True)

    def __str__(self):
        return self.content[:50]


class Label(models.Model):
    name = models.CharField(max_length=100)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='labels')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
