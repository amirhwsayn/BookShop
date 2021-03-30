from rest_framework import serializers
from .models import Token, User, Books, Files, ADS, Comment, Author, Category


class Serializer_File(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        Files_File = {
            "uuid": instance.File_UUID,
            "url": representation.pop("Files_File"),
            "size": instance.Files_File.size,
            "name": instance.File_Name,
            "format": instance.Files_File.name[-4:]
        }
        representation = Files_File
        return representation


class Serializer_File_Free(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        Files_File = {
            "size": instance.Files_File.size,
            "name": instance.File_Name,
            "format": instance.Files_File.name[-4:]
        }
        representation = Files_File
        return representation


class Serializer_Author(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'Author_Name',
            'Author_Description',
            'Author_ProfileImage',
        ]


class Serializer_Token(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            'Token_Token',
            'Token_CreateDate',
            'Token_User_Id',
            'Token_User_Email',
            'Token_User_Password',
        ]
        read_only_fields = ('Token_Code', 'Token_Token', 'Token_CreateDate')


class Serializer_Comments(serializers.ModelSerializer):
    class Serializer_User_C(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                'User_Name',
            ]

    sender = Serializer_User_C(source='user_set', many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            'Comment_Massage',
            'Comment_Like',
            'sender'
        ]


class Serializer_Book(serializers.ModelSerializer):
    Book_File_Get = Serializer_File(source='Book_File', many=True, read_only=True)
    Book_Preview_Get = Serializer_File(source='Book_Preview', many=True, read_only=True)
    Book_Content_Get = Serializer_File(source='Book_Content', many=True, read_only=True)
    Book_Comments_Get = Serializer_Comments(source='Book_Comments', many=True, read_only=True)
    Book_Author_Get = Serializer_Author(source='author_books', many=True, read_only=True)

    class Meta:
        model = Books
        fields = [
            # book data
            'Book_Token',
            'Book_Name',
            'Book_Description',
            'Book_Price',
            'Book_CreateDate',
            # Get Data
            'Book_File_Get',
            'Book_Preview_Get',
            'Book_Content_Get',
            'Book_Comments_Get',
            'Book_Author_Get'
        ]


class Serializer_Book_Free(serializers.ModelSerializer):
    Book_File_Get = Serializer_File_Free(source='Book_File', many=True, read_only=True)
    Book_Preview_Get = Serializer_File(source='Book_Preview', many=True, read_only=True)
    Book_Content_Get = Serializer_File_Free(source='Book_Content', many=True, read_only=True)
    Book_Comments_Get = Serializer_Comments(source='Book_Comments', many=True, read_only=True)
    Book_Author_Get = Serializer_Author(source='author_books', many=True, read_only=True)

    class Meta:
        model = Books
        fields = [
            # book data
            'Book_Token',
            'Book_Name',
            'Book_Description',
            'Book_Price',
            'Book_CreateDate',
            # Get Data
            'Book_File_Get',
            'Book_Preview_Get',
            'Book_Content_Get',
            'Book_Comments_Get',
            'Book_Author_Get'
        ]


class Serializer_ADS(serializers.ModelSerializer):
    Image = Serializer_File(source='ADS_Image', read_only=True, many=True)
    Book = Serializer_Book_Free(source='ADS_Book', read_only=True, many=True)

    class Meta:
        model = ADS
        fields = [
            'ADS_Title',
            'Book',
            'Image',
        ]


class Serializer_User(serializers.ModelSerializer):
    saved_books = Serializer_Book_Free(source='User_Saved_Books', many=True, read_only=True)
    rented_book = Serializer_Book(source='User_Rented_Books', many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'User_Token',
            'User_Id',
            'User_Password',
            'User_Email',
            'User_Credit',
            'User_Name',
            'User_CreateDate',
            'saved_books',
            'rented_book',
        ]


class Serializer_Category(serializers.ModelSerializer):
    CategoryImage = Serializer_File(source='Category_Image', many=True, read_only=True)
    CategoryBooks = Serializer_Book_Free(source='Category_Books', many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'Category_Name',
            'Category_Description',
            'CategoryImage',
            'CategoryBooks',
        ]
