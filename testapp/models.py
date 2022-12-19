import datetime
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


#https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
#Link to profile page model and view tutorial
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default = "John Wick")
    years = (
        ('First', '1st'),
        ('Second', '2nd'),
        ('Third', '3rd'),
        ('Fourth', '4th'),
        ('Other', 'Other'),
    )
    year = models.CharField(max_length=6,choices = years, default = 'First')
    major = models.CharField(max_length=100, default = 'CS')
    friends = models.ManyToManyField(User, related_name = 'friends', blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
   if created:
      Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
   instance.profile.save()

class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_text = models.TextField()
    pub_date =  models.DateTimeField('date published', auto_now_add=True)
    book_ISBN = models.CharField(max_length=13, default = '')
    # sell_status = models.BooleanField(default=False)
    # deptList = (
    #     ('BME', 'Biomedical Engineering'),
    #     ('CHE', 'Chemical Engineering'),
    #     ('CS', 'Computer Science'),
    #     ('ECE', 'Electrical and Computer Engineering'),
    #     ('STS', 'Engineering and Society'),
    #     ('MSE', 'Material Sciences Engineering'),
    #     ('MAE', 'Mechanical and Aerospace Engineering'),
    #     ('SYS', 'Systems Engineering'),
    #     ('CE', 'Civil Engineering'),
    #     ('APMA', 'Applied Mathematics'),
    # )
    # associated_dept = models.CharField(max_length = 4, choices = deptList, default='CS')
    associated_dept = models.CharField(max_length=50)
    course_id = models.CharField(max_length = 4, default='')
    favorite = models.ManyToManyField(User, related_name = 'favorite_post', blank=True)
    post_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.post_title

    def was_published_recently(self):
        now = datetime.timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class ClassSubject(models.Model):
    class_subject = models.CharField(max_length = 50)
    def __str__(self):
        return self.class_subject

#https://legionscript.medium.com/building-a-social-media-app-with-django-and-python-part-14-direct-messages-pt-1-1a6b8bd9fc40
#General guidance on messaging models and constructing messaging urls
class Thread(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    subject_text = models.CharField(max_length=500, default="No subject")
    was_read = models.BooleanField(default=False)

class Message(models.Model):
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE, related_name='+')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    message_text = models.CharField(max_length=1500)
    sent_date = models.DateTimeField('date sent', auto_now_add=True)
    was_read = models.BooleanField(default=False)

# class FavoritePost(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favoritepost", null=True)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     favorite = models.BooleanField