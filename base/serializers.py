from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product,OrderItem,Order,ShippingAddress,Review
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(read_only=True)
    _id=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model= User
        fields=["id","_id","username","email","name","isAdmin"]
    def get_name(self,obj):
        name=obj.first_name
        if name=="":
            name=obj.email
        return name
        
    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff

class UserSerializerWithToken(UserSerializer):
    token=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model= User
        fields=["id","_id","username","email","name","isAdmin","token"]

    def get_token(self,obj):
        token=RefreshToken.for_user(obj)
        return str(token.access_token)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields='__all__'
class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model= Product
        fields='__all__'
    
    def get_reviews(self,obj):
        reviews=obj.review_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return serializer.data



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= OrderItem
        fields='__all__'

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model= ShippingAddress
        fields='__all__'
class OrderSerializer(serializers.ModelSerializer):
    orderItems=serializers.SerializerMethodField(read_only=True)
    user=serializers.SerializerMethodField(read_only=True)
    shippingAddress=serializers.SerializerMethodField(read_only=True)
    paidAt = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    createdAt = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    deliverdAt= serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model= Order
        fields='__all__'
    
    def get_orderItems(self,obj):
        items=obj.orderitem_set.all()
        serializer=OrderItemSerializer(items,many=True)
        return serializer.data
    def get_shippingAddress(self,obj):
        try:
            address=ShippingAddressSerializer(obj.shippingaddress,many=False).data
        except:
            address= False
        
        return address

    def get_user(self,obj):
        user=obj.user
        serializer=UserSerializer(user,many=False)
        return serializer.data

    def get_paidAt(self,obj):
        return obj.paidAt
    def get_createdAt(self,obj):
        return obj.createdAt
    def get_deliverdAt(self,obj):
        return obj.deliverdAt



'''

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)
'''