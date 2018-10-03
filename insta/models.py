from django.db import models

# Create your models here.
class Profile(models.Model):
  profile_pic = models.ImageField(upload_to='images/')
  name = models.CharField(max_length=50)
  bio = models.TextField()

  def __str__(self):
    return self.name

  def save_profile(self):
    self.save()

  def update_profile(self):
    self.update()

  def delete_profile(self):
    self.delete()

  @classmethod
  def search_user(cls, name):
      info = cls.objects.filter(profile__name__icontains=name)
      return info

class Image(models.Model):
  name = models.CharField(max_length=50)
  image = models.ImageField(upload_to = 'images/')
  caption = models.TextField()
  profile = models.ForeignKey(Profile)

  def __str__(self):
      return self.name

  def save_image(self):
    self.save()

  def delete_image(self):
    self.delete()

  def update_caption(self):
    self.update()






