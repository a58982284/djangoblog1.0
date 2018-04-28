
import markdown
from django.utils.html import strip_tags
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    #下面这些都是字段
    title = models.CharField(max_length=70)
    body = models.TextField()
    excerpt = models.CharField(max_length=200,blank=True)
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
#返回的是post对应的url
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md =markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post,self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time','title']