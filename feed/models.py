from django.db import models

# Create your models here.
class Post(models.Model):
    text = models.CharField(max_length=240)

    # Creating a new date/time field
    # auto_now = True means field is non-editable and automatically populated upon
    # data entry
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[0:100] 
