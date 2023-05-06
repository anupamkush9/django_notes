from decimal import Decimal
from django.shortcuts import render
from cbvApp.models import Student
from cbvApp.serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404, HttpResponse

from rest_framework import generics,mixins
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .models import Customer, Purchase
from django.db import transaction


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        """
            URL for list method : 127.0.0.1:8000/students/
        """
        return Response({"msg":"This is a msg from custom list method."})
    
    def create(self, request, *args, **kwargs):
        """
            URL for create method : 127.0.0.1:8000/students/
        """
        return Response({"msg":"This is a msg from custom create method."})
    
    def update(self, request, *args, **kwargs):
        """
            URL for Retrieve method : 127.0.0.1:8000/students/2/
        """
        return Response({"msg":"This is a msg from custom update method."})
    
    def retrieve(self, request, *args, **kwargs):
        """
            URL for Retrieve method : 127.0.0.1:8000/students/2
        """
        return Response({"msg":"This is a msg from custom retrieve method."})
    
    def delete(self, request, *args, **kwargs):
        """
            URL for delete method : 127.0.0.1:8000/students/
        """
        return Response({"msg":"This is a msg from custom delete method."})
       
def atomic_transaction_view(request):
    try:
        with transaction.automic():
            """
                If there is an error during either of these two save operations, 
                the entire transaction will be rolled back and no changes will be made to the database.
                This ensures that each purchase is consistent and that the customer's balance is always accurate
            """
            customer = Customer.objects.get(id=1)
            purchase = Purchase()
            purchase.customer   = customer
            purchase.price = Decimal(10.00)
            customer.balance -= purchase.price
            customer.save()
            purchase.item= 'qwerty' + 1234
            purchase.save()
    except Exception as e:
        print("There is an error in atomic transaction view.",e)
        
    return HttpResponse("<h1>This is a msg from atomic transaction</h1>")

"""
class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class= StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class= StudentSerializer


class StudentList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class= StudentSerializer

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class StudentDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class= StudentSerializer

    def get(self,request,pk):
        return self.retrieve(request,pk)

    def put(self,request,pk):
        return self.update(request,pk)

    def delete(self,request,pk):
        return self.destroy(request,pk)


# Create your views here.
class StudentList(APIView):

    def get(self,request):
        students = Student.objects.all()
        serializer = StudentSerializer(students,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class StudentDetail(APIView):
    def get_object(self,pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(sefl,request,pk):
        student=self.get_object(pk)
        serializer=StudentSerializer(student,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
