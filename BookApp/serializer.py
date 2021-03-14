from rest_framework import serializers
from .models import Token, User, Books, Files, ADS, Comment


class Serializer_File(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'


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


class Serializer_User(serializers.ModelSerializer):
    comments = Serializer_Comments(source='User_Comments', many=True, read_only=True)

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
            'comments'
        ]


class Serializer_Book_Rent(serializers.ModelSerializer):
    Book_File_Get = Serializer_File(source='Book_File', many=True, read_only=True)
    Book_Preview_Get = Serializer_File(source='Book_Preview', many=True, read_only=True)
    Book_Content_Get = Serializer_File(source='Book_Content', many=True, read_only=True)
    Book_Comments_Get = Serializer_Comments(source='Book_Comments', many=True, read_only=True)

    class Meta:
        model = Books
        fields = [
            # book data
            'Book_Token',
            'Book_Name',
            'Book_Description',
            # Get Data
            'Book_File_Get',
            'Book_Preview_Get',
            'Book_Content_Get',
            'Book_Comments_Get'
        ]


class Serializer_Book(serializers.ModelSerializer):
    Book_Preview_Get = Serializer_File(source='Book_Preview', many=True, read_only=True)
    Book_Comments_Get = Serializer_Comments(source='Book_Comments', many=True, read_only=True)

    class Meta:
        model = Books
        fields = [
            # book data
            'Book_UUID',
            'Book_Name',
            'Book_Description',
            # Get Data
            'Book_Preview_Get',
            'Book_Comments_Get',
        ]


class Serializer_ADS(serializers.ModelSerializer):
    Image = Serializer_File(source='ADS_Image', read_only=True, many=True)
    Book = Serializer_Book(source='ADS_Book', read_only=True, many=True)

    class Meta:
        model = ADS
        fields = [
            'ADS_Title',
            'Book',
            'Image',
        ]
