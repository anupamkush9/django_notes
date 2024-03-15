from django.urls import path, include
from .views import download_file_on_the_go, webhook, bulk_create_test, for_loop_create_test, SendMailApiView, Home, index

urlpatterns = [
    path('download_file_on_the_go/<int:id>', download_file_on_the_go, name='download_file_on_the_go'),
    path('webhook/', webhook, name='webhook'),
    path('bulk_create_test/', bulk_create_test, name="bulk_create_test"),
    path('for_loop_create_test/', for_loop_create_test, name="for_loop_create_test"),
    path('send_mail/', SendMailApiView.as_view(), name="sendmail_view"),
    path('accounts/', include('allauth.urls')),
    path('/home', Home.as_view(), name="home"),
    path('', index, name="index"),
    
]
