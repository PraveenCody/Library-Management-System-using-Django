from django.db import models

# Create your models here.

class Book(models.Model):
    bookname = models.CharField(max_length=50)
    bookimg = models.ImageField(upload_to='book/')
    book = models.FileField(upload_to="bks/",)
    author = models.CharField(max_length=50,default='Unknown Author')
    desc = models.CharField(max_length=500)

    def __str__(self):
        return self.bookname
    
class Borrowed(models.Model):
    bookin = models.ForeignKey(Book,on_delete=models.CASCADE,null=True, blank=True)
    bookname = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    firstdate = models.DateField()
    lastdate = models.DateTimeField()

    def __str__(self):
        return self.username