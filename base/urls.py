from django.urls import path
from .views import( get_products,get_product,MyTokenObtainPairView,get_user_profile,
get_users,register_user,update_user_profile,addOrderItems,getOrderById,updateOrderToPaid,getMyOrders,
deleteUser,updateUser,getUserById,deleteProduct,createProduct,updateProduct,uploadImage,getOrders
,updateOrderToDelivered,createProductReview,getTopProducts,register_social_user
#FacebookLogin,#GoogleLogin,GoogleSocialAuthView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
 #   path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    # path('rest-auth/google', GoogleLogin.as_view(), name='google_login'),
  #  path('google/', GoogleSocialAuthView.as_view()),

    path('users/googlelogin', register_social_user, name='register_social_user'),

    path('users/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("users/profile/",get_user_profile,name="users-profile"),
    path("users/profile/update",update_user_profile,name="update-users-profile"),
    
    path("users/register",register_user,name="register"),
    path("users",get_users,name="users"),
    path("users/delete/<str:pk>",deleteUser,name="user-delete"),
    path("users/update/<str:pk>",updateUser,name="user-update"),
    path("users/<int:pk>",getUserById,name="user-by-id"),

    path("products",get_products,name="products"),
    path("products/top",getTopProducts,name="top-products"),
    path("products/create",createProduct,name="products-create"),
    path("products/upload/",uploadImage,name="image-upload"),
    path("products/<int:pk>/delete",deleteProduct,name="product-delete"),
    path("products/<int:pk>/",get_product,name="product"),
    path("products/<int:pk>/update",updateProduct,name="product-update"),
    path("products/<int:pk>/review",createProductReview,name="product-review"),

    path("orders/",getOrders,name="my-orders"),
    path("orders/add/",addOrderItems,name="order-items"),
    path("orders/myorders/",getMyOrders,name="my-orders"),
    path("orders/<int:pk>/",getOrderById,name="user-add"),
    path("orders/<int:pk>/pay/",updateOrderToPaid,name="update-to-paid"),
    path("orders/<int:pk>/deliver/",updateOrderToDelivered,name="update-to-delivered"),
]
