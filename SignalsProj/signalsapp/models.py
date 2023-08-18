from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from datetime import datetime
import json

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=200, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class TaskDate(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)

    
class History(models.Model):
    history = models.TextField(default='{}')
    

"""here pre_save signals generates the slug of insatnce name"""
# @receiver(pre_save, sender=Task)
def task_handler(sender, instance, **kwargs):
    print("pre_save signal called")
    print(sender)
    print(instance)
    print(instance.description)
    instance.slug = slugify(instance.name)

pre_save.connect(task_handler, sender=Task)


"""here post_save signals generates the date of task creation"""
@receiver(post_save, sender=Task)
def task_hander_post(sender, instance, **kwargs):
    print("post_save signal called")
    TaskDate.objects.create(task=instance.name, date=datetime.now())


"""here pre_delete method create a json format history before delete the object"""
@receiver(pre_delete, sender=Task)
def task_handeler_pre_delete(sender, instance, **kwargs):
    print("pre_delete signal get called")

    data = {'task': instance.name, 'desc': instance.description, 'slug': instance.slug}
    History.objects.create(history = json.dumps(data))



