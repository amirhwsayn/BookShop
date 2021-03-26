from django.core.exceptions import ObjectDoesNotExist
from django.urls import path
from rest_framework import generics, status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from .Actions import SendMail, errorBuild
from .Permissions import PERM_CreateUser, PERM_User, PERM_login
from .models import User, Token, Books, ADS, Category
from .serializer import Serializer_Token, Serializer_User, Serializer_Book, Serializer_ADS, Serializer_Comments, \
    Serializer_Book_Rent, Serializer_Category


# Create your views here.


class CreateToken(generics.CreateAPIView):
    serializer_class = Serializer_Token

    def create(self, request, *args, **kwargs):
        id = request.data['Token_User_Id']
        email = request.data['Token_User_Email']
        try:
            User.objects.get(User_Id=id)
            return errorBuild('این نام کاربری قبلا انتخاب شده')
        except ObjectDoesNotExist:
            try:
                User.objects.get(User_Email=email)
                return errorBuild('این پست الکترونیکی قبلا انتخاب شده')
            except ObjectDoesNotExist:
                return super().create(request, args, kwargs)

    def perform_create(self, serializer):
        obj = serializer.save()
        SendMail(obj.Token_Code, obj.Token_User_Email)


class CreateUser(APIView):
    permission_classes = [PERM_CreateUser]

    def get(self, request):
        token = Token.objects.get(Token_Token=request.headers['token'])
        id = token.Token_User_Id
        email = token.Token_User_Email
        password = token.Token_User_Password
        User.objects.create(
            User_Id=id,
            User_Email=email,
            User_Password=password
        )
        mdata = User.objects.filter(User_Id=id)
        ddata = Serializer_User(mdata, many=True)
        return Response(ddata.data, status=status.HTTP_200_OK)

    # def handle_exception(self, exc):
    #     if isinstance(exc, exceptions.PermissionDenied):
    #         return errorBuild('کد وارد شده نا معتبر است')


class LoginUser(generics.ListAPIView):
    permission_classes = [PERM_login]
    serializer_class = Serializer_User

    def get_queryset(self):
        id = self.request.headers['id']
        password = self.request.headers['password']
        return User.objects.filter(User_Id=id, User_Password=password)


class RecentBooks(generics.ListAPIView):
    permission_classes = [PERM_User]
    serializer_class = Serializer_Book
    queryset = Books.objects.all()[:20]


class SearchBook(generics.ListAPIView):
    permission_classes = [PERM_User]
    serializer_class = Serializer_Book

    def get_queryset(self):
        title = self.request.headers['key']
        return Books.objects.filter(Book_Name__startswith=title)


class GetADS(generics.ListAPIView):
    permission_classes = [PERM_User]
    queryset = ADS.objects.all()
    serializer_class = Serializer_ADS


class SendComment(generics.CreateAPIView):
    permission_classes = [PERM_User]
    serializer_class = Serializer_Comments

    def perform_create(self, serializer):
        obj = serializer.save()
        bookid = self.request.headers['bookid']
        userid = self.request.headers['token']
        Books.objects.get(Book_UUID=bookid).Book_Comments.add(obj)
        User.objects.get(User_Token=userid).User_Comments.add(obj)


class AddSavedBook(APIView):
    permission_classes = [PERM_User]

    def post(self, request):
        if 'bookid' in request.headers and 'token' in request.headers:
            bookid = request.headers['bookid']
            userid = request.headers['token']
            user = User.objects.get(User_Token=userid) \
                .User_Saved_Books
            try:
                user.add(Books.objects.get(Book_UUID=bookid))
            except ObjectDoesNotExist:
                return errorBuild("کتاب مورد نظر یافت نشد")
            return Response(status=status.HTTP_200_OK)
        else:
            return errorBuild("درخواست نا معتبر")

    # def handle_exception(self, exc):
    #     if isinstance(exc, exceptions.ValidationError):
    #         return errorBuild("درخواست نا معتبر")


class GetCategory(generics.ListAPIView):
    permission_classes = [PERM_User]
    queryset = Category.objects.all()
    serializer_class = Serializer_Category


class TEST(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = Serializer_Book_Rent


urls = [
    # Requirements
    # body -> {
    #       "Token_User_Id" : ""
    #       "Token_User_Email" : ""
    #       "Token_User_Password" : ""
    #   }
    # Description -> create register token
    # OK
    path('ct', CreateToken.as_view()),

    # Requirements
    # headers -> token:TokenTOKEN , code:TokenCODE
    # Description -> create user with token info
    # OK
    path('cu', CreateUser.as_view()),

    # Requirements :
    # headers -> token:UserToken
    # Description -> recent add book
    path('rb', RecentBooks.as_view()),

    # Requirements :
    # headers -> key:BookName , token:UserToken
    # Description -> search book with keyword
    path('sb', SearchBook.as_view()),

    # Requirements :
    # headers -> token:UserToken
    # Description -> get ads
    path('ga', GetADS.as_view()),

    # Requirements :
    # headers -> token:UserToken , bookid:BOOK_UUID
    # body -> {
    #       "Comment_Massage" : ""
    #       "Comment_Like" : ""
    #   }
    # Description -> create new comment for book
    path('sc', SendComment.as_view()),

    # Requirements :
    # headers -> token:UserToken , bookid:BOOK_UUID
    path('ab', AddSavedBook.as_view()),

    # Requirements :
    # headers -> token:UserToken
    path('gt', GetCategory.as_view()),

    # Requirements :
    # headers -> id:UserID , password:UserPassword
    path('lu', LoginUser.as_view()),


    path('t', TEST.as_view())

]
