from django.urls import path, include
from .views import ( HeartBeatAPIVIEW, create_mobile, custom_filter_view, custom_tag_view, download_file_on_the_go, feedback, list_files, bulk_create_test,
                    for_loop_create_test, SendMailApiView, Home, index,
                    AnnotateCategory, webhookApiView, FileDownloadApi )

urlpatterns = [
    path('download_file_on_the_go/<str:hash_id>', download_file_on_the_go, name='download_file_on_the_go'),
    path('list_files/', list_files, name='list_files'),
    # path('webhook/', webhook, name='webhook'),
    path('bulk_create_test/', bulk_create_test, name="bulk_create_test"),
    path('for_loop_create_test/', for_loop_create_test, name="for_loop_create_test"),
    path('send_mail/', SendMailApiView.as_view(), name="sendmail_view"),
    path('accounts/', include('allauth.urls')),
    # path('/home', Home.as_view(), name="home"),
    path('', Home.as_view(), name="home"),
    path('annotate/', AnnotateCategory.as_view(), name="annotate"),
    path('heartbeat/', HeartBeatAPIVIEW.as_view(), name="heartbeat"),
    path('feedback/', feedback, name='feedback'),
    path('without_forms/', create_mobile, name='create_mobile'),
    path('custom_filters/', custom_filter_view, name='custom_filters'),
    path('custom_tags/', custom_tag_view, name='custom_tags'),
    path('file-dowload-api/', FileDownloadApi.as_view(), name='file_download_api'),
    
]
