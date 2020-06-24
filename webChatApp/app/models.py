from django.db import models
from django.utils.timezone import now
from django.utils.timezone import localtime

# Create your models here.

class Todo(models.Model):
    user_id = models.IntegerField(null=False)
    todo_name = models.CharField(max_length=45,null=False)
    remark = models.CharField(max_length=300)
    regist_date = models.DateTimeField(default=now, null=False)
    scheduled_start_date = models.DateField(null=True)
    start_date = models.DateField(null=True)
    expected_end_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    status = models.IntegerField(null=False)

    class Meta:
        db_table = 'todo'


class Room(models.Model):
    #id = models.ImageField(primary_key=True)
    room_name = models.CharField(max_length=45,null=False)

    class Meta:
        db_table = 'room'


class Message(models.Model):
    room_no = models.IntegerField(primary_key=True,null=False)
    user_id = models.IntegerField(null=False)
    regist_date = models.DateField(null=False)
    regist_time = models.TimeField(null=False)
    message = models.CharField(null=True,max_length=300)
    kbn: models.CharField(null=False)
    file_path = models.CharField(null=False,max_length=300)

    class Meta:
        db_table = 'message'
