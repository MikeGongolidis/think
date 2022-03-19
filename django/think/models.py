from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    alien_form = models.CharField(max_length=50)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=300)

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,null=False, on_delete=models.CASCADE, related_name='answer')
    question_id = models.ForeignKey(Question, null=False, on_delete=models.CASCADE, related_name='question')
    answer_text = models.CharField(max_length=300)