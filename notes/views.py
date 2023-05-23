import json
import logging
from redis import Redis
import requests
import datetime
import pyrfc6266
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Files, Temp_Data_Bulk_Create, Category
from django.db.models import Count
# Django imports
from django.core.mail import send_mail
from django.conf import settings
# Rest Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from django.views import View
from .forms import Bookform
from .forms import FeedbackForm
from .models import Mobiles

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

class Home(View):
    def get(self, request):
        # return HttpResponse('<h1>response from get method<h1>')
        return render(request, 'notes/home.html', {"form":Bookform})
    
    def post(self, request):
        form = Bookform(request.POST, request.FILES)
        form.is_valid()
        form.save()
        return redirect('home')
    
def index(request):
    return render(request, 'notes/index.html')

class AnnotateCategory(View):
    def get(self, request):
        category = Category.objects.annotate(no_of_prods=Count('product'))
        s = category.query
        final_string = ''
        for cat in category:
            final_string += f"<br><br>{cat.name} has {cat.no_of_prods} no_of_prods."
        return HttpResponse(str(s)+'\n'+final_string)

class HeartBeatAPIVIEW(APIView):
    def get(self, request):
        redis_obj = Redis(host="127.0.0.1", port=6379)
        response_data = ""
        source = ""
        response_data = redis_obj.get('resp')
        if response_data:
            # source = 'cache'
            source = "Cache"
            print("inside try block..")
            return Response({"response_msg": json.loads(response_data), "source": source})
        else:
            # irs_object = CrawlerSettings.objects.filter(name="crawler_is_irs_tin_service_unavailable").first()
            # updating in cache
            cache_expiry_time = datetime.timedelta(minutes=1)
            try:
                redis_obj.set("resp", json.dumps({'status': "Message from database",
                                            'last_updated': str(datetime.datetime.now())}), ex=cache_expiry_time)
                response_data = "Response from server"
                source = "Database"
                print("Inside else block..")
                return Response({"response_msg" : {"status" : response_data,'last_updated': str(datetime.datetime.now())},
                                "source": source})
            except Exception as e:
                print('Exception in update_service_status_in_cache: ', e)
        return Response({"response_msg": "some Thing went wrong", "source": source})


def feedback(request):
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a success page
        try:
            print(form.errors)
        except:
            pass
    return render(request, 'notes/feedback.html', {'form': form})


def custom_filter_view(request):
    context = {"number1": 10, "number2":20, "number3":30, "name":"Anupam"}
    return render(request, 'notes/my_custom_filters.html', context)

def custom_tag_view(request):
    context = {"number1": 10, "number2":20, "number3":30, "name":"Anupam"}
    return render(request, 'notes/my_custom_tags.html', context)



from django.shortcuts import render, redirect
from .models import Mobiles

def create_mobile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        image = request.FILES.get('image')  # Get the uploaded image file
        form = {
            'name': name,
            'brand': brand,
            'price': price
        }
        errors = {}

        if not name:
            errors['name'] = 'Name is required.'
        if not brand:
            errors['brand'] = 'Brand is required.'
        if not price:
            errors['price'] = 'Price is required.'
        if not image:
            errors['image'] = 'Image is required.'

        if Mobiles.objects.filter(name=name).exists():
            errors['name'] = 'Mobile with the same name already exists.'

        if errors:
            context = {
                'form': form,
                'errors': errors
            }
            return render(request, 'notes/without_foams.html', context)
        else:
            Mobiles.objects.create(name=name, brand=brand, price=price, image=image)  # Save the image field
            return redirect('home')
    else:
        context = {}
        return render(request, 'notes/without_foams.html', context)
