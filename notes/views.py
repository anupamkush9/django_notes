import logging
import requests
import datetime
import pyrfc6266
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Files, Temp_Data_Bulk_Create
# Django imports
from django.core.mail import send_mail
from django.conf import settings
# Rest Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

logger = logging.getLogger(__name__)


def download_file_on_the_go(request, id):
    """
    file url => https://www.some-website.com/url-to-destination-file
    encoded url => https://www.my-website.com/<uuid>

    The objective of this function to encode urls and provide files on the go
    """
    logger.warning("hello world")
    # url = "https://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf"
    # url = "https://www.businessregistry.gr/downloadFile/index?key=assemblyDecision&elementId=3113977"
    url = "https://file-examples.com/storage/fe863385e163e3b0f92dc53/2017/10/file_example_JPG_100kB.jpg"#Files.objects.filter(id=id).first().url

    file = requests.get(url)
    try:
        file_name = pyrfc6266.requests_response_to_filename(file)
        logger.info("File name: ", str(file))
    except Exception as e:
        file_name = str(datetime.datetime.now())
        logger.warning("Exception while getting file name: ", str(e))
    response = HttpResponse(file)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
    response['Content-Type'] = "application/octet-stream"
    return response


def webhook(request):
    # internal api
    url = 'https://www.boredapi.com/api/activity'
    response = requests.get(url)

    print(response.json())

    # webhook api
    webhook_url = 'https://webhook.site/d2174683-f508-462c-8eae-0e4b94dc90c1'
    requests.post(webhook_url, json=response.json())

    print("success")

    return HttpResponse("<h1 style='color: green; font= '>Success</h1>")


def for_loop_create_test(request):
    """
    for loop Create in django is used to insert bulk records in batch size
    """
    start = datetime.datetime.now()
    print()
    for i in range(1000):
        print(i)
        Temp_Data_Bulk_Create.objects.create(name=f"name{i}", age=i)

    end = datetime.datetime.now()
    message = {"Time required": str(end - start)}

    return JsonResponse(message)


def bulk_create_test(request):
    """
    Bulk Create in django is used to insert bulk records in batch size
    """
    start = datetime.datetime.now()

    users = [Temp_Data_Bulk_Create(name="hello", age=i) for i in range(1000)]
    Temp_Data_Bulk_Create.objects.bulk_create(users)

    end = datetime.datetime.now()
    message = {"Time required": str(end - start)}

    return JsonResponse(message)

    # {"Time required": "0:02:01.423410"} for 50k using for loop
    # {"Time required": "0:04:40.000341"} for 100k using for loop
    # {"Time required": "0:00:19.443909"} for 1 Million using for loop

    # {"Time required": "0:00:01.058299"} for 50k using bulk create and list comprehension BS=50k
    # {"Time required": "0:00:01.975993"} for 100k using bulk create and list comprehension BS=50k
    # {"Time required": "0:00:19.443909"} for 1 Million using bulk create and list comprehension BS=50k


class MailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=998)
    message = serializers.CharField(max_length=10000)
    recipient = serializers.EmailField()


class SendMailApiView(APIView):

    def send_gmail(self, subject, message, recipients):
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipients, fail_silently=False)
        return None

    def post(self, request):
        data = request.data
        print("sending mail...")
        serializer = MailSerializer(data=data, many=False)
        if serializer.is_valid():
            print("validated")
            try:
                subject = data['subject']
                message = data['message']
                recipient = data['recipient']
                self.send_gmail(subject, message, [recipient, ])
                return Response({"message": "Mail sent successfully!"}, status=200)
            except Exception as e:
                return Response({"message": str(e)}, 400)
        return Response({"message": serializer.errors}, 400)
