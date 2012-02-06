from django.db import models
from django.core.files import storage
from django.conf import settings

class NoDeleteFileStorage(storage.FileSystemStorage):
    def delete(self, name):
        pass

ndfs = NoDeleteFileStorage()

class BannerImage(models.Model):
    image = models.ImageField(upload_to="uploads/shared/banners",
                              null = True, blank = True, storage = ndfs)

    def __unicode__(self):
        return str(self.image.name)

    def image_width(self):
        return self.image.width

    def image_height(self):
        return self.image.height

    def dimentions(self):
        return (str(self.image.width) + 'x' + str(self.image.height))

    def get_image_url(self):
        return (str(settings.MEDIA_URL)+str(self.image.name))


class Banner(models.Model):
    name = models.CharField(max_length=250, null=True)
    images = models.ManyToManyField(BannerImage)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return ('Banner: '+str(self.name))

    def get_images(self):
        return self.images