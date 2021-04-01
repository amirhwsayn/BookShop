from uuid import uuid4

from django.db import models

from BookApp.Randoms import Random_Token, Random_Name, Random_Code


# Create your models here.
class Files(models.Model):
    File_UUID = models.UUIDField(default=uuid4, primary_key=True)
    File_Name = models.CharField(max_length=50, default='null')
    Files_File = models.FileField(upload_to='file/')


class Comment(models.Model):
    Comment_Token = models.TextField(max_length=100, unique=True, default=Random_Token, primary_key=True)
    Comment_Massage = models.TextField(max_length=200)
    Comment_Like = models.BooleanField()


class Books(models.Model):
    Book_Token = models.TextField(max_length=100, unique=True, default=Random_Token, primary_key=True)
    Book_UUID = models.UUIDField(default=uuid4)
    Book_Name = models.CharField(max_length=50)
    Book_Cover = models.ImageField(upload_to='file/', blank=True)
    Book_Description = models.TextField(max_length=300, blank=True)
    Book_Price = models.IntegerField(default=0)
    Book_CreateDate = models.DateTimeField(auto_now=True)
    Book_File = models.ManyToManyField(Files, related_name='book_files')
    Book_Preview = models.ManyToManyField(Files, related_name='book_preview', blank=True)
    Book_Content = models.ManyToManyField(Files, related_name='book_content', blank=True)
    Book_Comments = models.ManyToManyField(Comment, blank=True, related_name='comments')

    def __str__(self):
        return self.Book_Name


class ADS(models.Model):
    ADS_UUID = models.UUIDField(default=uuid4, primary_key=True)
    ADS_Title = models.TextField(max_length=300)
    ADS_Image = models.ManyToManyField(Files, related_name='ads_image')
    ADS_Book = models.ManyToManyField(Books, blank=True, related_name='ads_book')

    def __str__(self):
        return self.ADS_Title


class Author(models.Model):
    Author_Token = models.TextField(max_length=100, unique=True, default=Random_Token, primary_key=True)
    Author_Id = models.CharField(max_length=50, unique=True)
    Author_Password = models.CharField(max_length=50)
    Author_Email = models.EmailField(unique=True)
    Author_Name = models.CharField(max_length=50, default=Random_Name)
    Author_Description = models.TextField(max_length=300, blank=True)
    Author_ProfileImage = models.ImageField(upload_to='file/', blank=True)
    Author_CreateDate = models.DateTimeField(auto_now=True)
    Author_Books = models.ManyToManyField(Books, blank=True, related_name='author_books')
    Author_Files = models.ManyToManyField(Files, blank=True, related_name='author_files')


class User(models.Model):
    User_Token = models.TextField(max_length=100, unique=True, default=Random_Token, primary_key=True)
    User_Id = models.CharField(max_length=50, unique=True)
    User_Password = models.CharField(max_length=50)
    User_Email = models.EmailField(unique=True)
    User_Credit = models.IntegerField(default=0)
    User_Name = models.CharField(max_length=50, default=Random_Name)
    User_CreateDate = models.DateTimeField(auto_now=True)
    User_Rented_Books = models.ManyToManyField(Books, blank=True)
    User_Saved_Books = models.ManyToManyField(Books, blank=True, related_name='User_Saved_Books')
    User_Comments = models.ManyToManyField(Comment, blank=True)


class Category(models.Model):
    Category_Name = models.CharField(max_length=20)
    Category_Image = models.ManyToManyField(Files)
    Category_Description = models.TextField(max_length=100)
    Category_Books = models.ManyToManyField(Books)


class Token(models.Model):
    # Token Data
    Token_Token = models.TextField(max_length=100, unique=True, default=Random_Token)
    Token_Code = models.CharField(max_length=6, default=Random_Code)
    Token_CreateDate = models.DateTimeField(auto_now=True)
    # User Data
    Token_User_Email = models.EmailField()
    Token_User_Id = models.CharField(max_length=50)
    Token_User_Password = models.CharField(max_length=50)
