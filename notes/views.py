import logging
import requests
import datetime
import pyrfc6266
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Files, Temp_Data_Bulk_Create
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
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


class webhookApiView(APIView):

    def post(self, request):
        '''
        curl --location '127.0.0.1:8000/notes/webhook/' \
            --header 'Content-Type: application/json' \
            --data '{
                "webhook_urls": "https://webhook.site/09b75120-f3a6-4cd9-bfd9-33c0040dfbf2"
            }'
        '''
        # internal api
        url = 'https://www.boredapi.com/api/activity'
        response = requests.get(url)

        print(response.json())

        # webhook api
        webhook_urls = request.data.get('webhook_urls')
        if not webhook_urls:
            return Response({'error': 'webhook_urls is required'}, status=status.HTTP_400_BAD_REQUEST)

        requests.post(webhook_urls, json=response.json())

        print("success")
        
        return Response(response.json(), status=status.HTTP_201_CREATED)



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

