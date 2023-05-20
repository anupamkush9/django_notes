from django.urls import path
from .views import download_file_on_the_go, webhookApiView, bulk_create_test, for_loop_create_test

urlpatterns = [
    path('download_file_on_the_go/<int:id>', download_file_on_the_go, name='download_file_on_the_go'),
    path('webhook/', webhookApiView.as_view(), name='webhook'),
    path('bulk_create_test/', bulk_create_test, name="bulk_create_test"),
    path('for_loop_create_test/', for_loop_create_test, name="for_loop_create_test")

]
