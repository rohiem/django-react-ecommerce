from django.shortcuts import render
from .models import Product,Order,OrderItem,ShippingAddress,Review
from .serializers import ProductSerializer,UserSerializer,UserSerializerWithToken,OrderSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from datetime import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
# from .serializers import GoogleSocialAuthSerializer
from django.contrib.auth import authenticate, login

'''
class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
'''
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data=super().validate(attrs)
        serializer=UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(["POST"])
def register_social_user(request):
    data=request.data

    if not User.objects.filter(email=data["email"]).exists():
        data=request.data

        user=User.objects.create(
            first_name=data["name"],
            username=data["email"],
            email=data["email"],
            password=make_password(data["password"])
        )
        serializer=UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    else:
        data=request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            serializer=UserSerializerWithToken(user,many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def register_user(request):
    try:
        data=request.data
        user=User.objects.create(
            first_name=data["name"],
            username=data["email"],
            email=data["email"],
            password=make_password(data["password"])
        )
        serializer=UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    except:
        message={"detail":"the email provided already exist"}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def get_user_profile(request):
    user=request.user
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)



@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def update_user_profile(request):
    user=request.user
    data=request.data
    user.first_name = data['name']
    user.username=data["email"]
    user.email=data["email"]
    if data["password"]!="":
        user.password=make_password(data["password"])
    user.save()
    serializer=UserSerializerWithToken(user,many=False)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAdminUser,])
def get_users(request):
    users=User.objects.all()
    serializer=UserSerializer(users,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_products(request):
    query=request.query_params.get("keyword")
    if query == None:
        query=""
    products=Product.objects.filter(name__icontains=query).order_by("-_id")
    page=request.query_params.get("page")
    paginator=Paginator(products,4)
    try:
        products=paginator.page(page)
    except PageNotAnInteger:
        products=paginator.page(1)
    except EmptyPage:
        products=paginator.page(paginator.num_pages)
    
    if page==None:
        page=1
    page=int(page)



    serializer=ProductSerializer(products,many=True)
    return Response({"products":serializer.data,"page":page,"pages":paginator.num_pages})


@api_view(["GET"])
def getTopProducts(request):
    products=Product.objects.filter(rating__gte=3.5).order_by("-rating")[:4]
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)
@api_view(["GET"])
def get_product(request,pk):
    product=Product.objects.get(_id=pk)
    serializer=ProductSerializer(product,many=False)
    return Response(serializer.data)

@api_view(["DELETE"])
def deleteProduct(request,pk):
    product=Product.objects.get(_id=pk)
    product.delete()
    return Response("product was deleted")

@api_view(["POST"])
@permission_classes([IsAuthenticated,])
def addOrderItems(request):
    user=request.user
    data=request.data
    orderItems=data["orderItems"]
    if orderItems and len(orderItems)==0:
        return Response({"detail":"no order items"},status=status.HTTP_400_BAD_REQUEST)
    else:
        order =Order.objects.create(
            user =user,
            paymentMethod=data["paymentMethod"],
            taxPrice=data["taxPrice"],
            shippingPrice=data["shippingPrice"],
            totalPrice=data["totalPrice"]
        )
        shipping=ShippingAddress.objects.create(
            order=order,
            address=data["shippingAddress"]["address"],
            city=data["shippingAddress"]["city"],
            postalCode=data["shippingAddress"]["postalCode"],
            country=data["shippingAddress"]["country"],
        )
        for i in orderItems:
            product=Product.objects.get(_id=i["product"])
            item=OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i["qty"],
                price=i["price"],
                image=product.image.url
            )

            product.countInStock -= int(item.qty)
            product.save()
        serializer=OrderSerializer(order,many=False)
        return Response(serializer.data)
@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def getOrderById(request,pk):
    user=request.user
    try:
        order=Order.objects.get(_id=pk)
        if user.is_staff or order.user==user:
            serializer=OrderSerializer(order,many=False)
            return Response(serializer.data)
        else:
            return Response({"detail":"not authorized to view this order"},status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"detail":"order does not exist"},status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def updateOrderToPaid(request,pk):
    order =Order.objects.get(_id=pk)
    order.isPaid=True
    order.paidAt = datetime.now()
    order.save()
    return Response("order was paid")




@api_view(["PUT"])
@permission_classes([IsAdminUser,])
def updateOrderToDelivered(request,pk):
    order =Order.objects.get(_id=pk)
    order.isDelivered=True
    order.deliverdAt = datetime.now()
    order.save()
    return Response("order was delivered")



@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def getMyOrders(request):
    user=request.user
    orders=user.order_set.all()
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)





@api_view(["GET"])
@permission_classes([IsAdminUser,])
def getOrders(request):
    orders=Order.objects.all()
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)






@api_view(["DELETE"])
@permission_classes([IsAdminUser,])
def deleteUser(request,pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response("the user was deleted")



@api_view(["GET"])
@permission_classes([IsAdminUser,])
def getUserById(request,pk):
    user=User.objects.get(id=pk)
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)



@api_view(["PUT"])
@permission_classes([IsAdminUser,])
def updateUser(request,pk):
    user=User.objects.get(id=pk)
    data=request.data
    user.first_name = data['name']
    user.username=data["email"]
    user.email=data["email"]
    user.is_staff=data["isAdmin"]

    user.save()
    serializer=UserSerializer(user,many=False)

    return Response(serializer.data)





@api_view(["POST"])
@permission_classes([IsAdminUser,])
def createProduct(request):
    user=request.user
    data=request.data


    product=Product.objects.create(
                user=user,
                name=data["name"],
                image=request.FILES.get("image"),
                description=data["description"],
                brand=data["brand"],
                price=data["price"],
                countInStock=data["countInStock"],
                category=data["category"]

            )

    serializer=ProductSerializer(product,many=False)
    return Response(serializer.data)




@api_view(["put"])
@permission_classes([IsAdminUser,])
def updateProduct(request,pk):

    product=Product.objects.get(_id=pk)

    user=request.user
    data=request.data
    product.user=user
    product.name=data["name"]
    product.image=data["image"]
    product.description=data["description"]
    product.brand=data["brand"]
    product.price=data["price"]
    product.countInStock=data["countInStock"]
    product.category=data["category"]
    product.save()

            

    serializer=ProductSerializer(product,many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser,])
def uploadImage(request):
    data=request.data
    product_id=data["product_id"]
    product=Product.objects.get(_id=product_id)
    product.image=request.FILES.get("image")
    product.save()
    return Response(product.image.url)

@api_view(["POST"])
@permission_classes([IsAuthenticated,])
def createProductReview(request,pk):
    product=Product.objects.get(_id=pk)
    user=request.user
    data=request.data
    # review already exists
    alreadyExists=product.review_set.filter(user=user).exists()
    if alreadyExists:
        content={"detail":"product already reviewed"}
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
    # review with no rating
    elif data["rating"]==0:
        content={"detail":"please select a rating"}
        return Response(content,status=status.HTTP_400_BAD_REQUEST)

    # create review
    else:
        review=Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data["rating"],
            comment=data["comment"]
        )
        reviews=product.review_set.all()
        product.numReviews=len(reviews)

        total=0
        for i in reviews:
            total+=i.rating

        product.rating=total/len(reviews)
        product.save()
    content={"detail":"review was added"}
    return Response(content,status=status.HTTP_200_OK)