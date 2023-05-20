from django.urls import path, include
from .views import ( HeartBeatAPIVIEW, download_file_on_the_go, feedback, webhook, bulk_create_test,
                    for_loop_create_test, SendMailApiView, Home, index,
                    AnnotateCategory )

urlpatterns = [
    path('download_file_on_the_go/<int:id>', download_file_on_the_go, name='download_file_on_the_go'),
    path('webhook/', webhook, name='webhook'),
    path('bulk_create_test/', bulk_create_test, name="bulk_create_test"),
    path('for_loop_create_test/', for_loop_create_test, name="for_loop_create_test"),
    path('send_mail/', SendMailApiView.as_view(), name="sendmail_view"),
    path('accounts/', include('allauth.urls')),
    # path('/home', Home.as_view(), name="home"),
    path('', Home.as_view(), name="home"),
    path('annotate/', AnnotateCategory.as_view(), name="annotate"),
    path('heartbeat/', HeartBeatAPIVIEW.as_view(), name="heartbeat"),
    path('feedback/', feedback, name='feedback'),
    
]
