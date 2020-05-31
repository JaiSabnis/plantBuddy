from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
   text = models.CharField(max_length=2000, blank=False)

class Post(models.Model):
   title = models.CharField(max_length=25, blank=True)
   text = models.CharField(max_length=2000, blank=False)
   comments = models.ManyToManyField(Comment,related_name="comments", blank=True)

   def __str__(self):
      return f"{self.title}"


class Plant(models.Model):
   name = models.CharField(max_length=25, blank=False)
   about = models.CharField(max_length=2000, blank=True)
   careBuddies = models.ManyToManyField(User, related_name="fans", blank=True)
   posts = models.ManyToManyField(Post,related_name="posts", blank=True)
   def __str__(self):
      return f"{self.name}"

class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   first = models.CharField(max_length=20, blank=True)
   last = models.CharField(max_length=20, blank=True)
   bio = models.CharField(blank=True, max_length=2000)
   birthdate = models.DateField(blank=True)
   friendRequests = models.ManyToManyField(User, related_name="requests", blank=True)
   friends = models.ManyToManyField(User, related_name="friends", blank=True)
   plants = models.ManyToManyField(Plant, related_name="plants", blank=True)
   def __str__(self):
       return f"{self.user}"



