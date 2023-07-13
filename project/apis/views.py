from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveDestroyAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


#hyper viewset
class employeehyperviewset(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=employeehyperserializer

#modal viewset
class employeemodalviewset(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    # authentication_classes=[BasicAuthentication]
    # permission_classes=[IsAuthenticated]
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAdminUser]


#viewset
class employeeviewset(viewsets.ViewSet):
    def list(self,request):
        employee_obj=Employee.objects.all()
        serializers=EmployeeSerializer(employee_obj,many=True)
        return Response({'status':200,"payload":serializers.data})
    def retrieve(self,request,pk=None):
        id=pk
        if id is not None:
            employee_obj=Employee.objects.get(id=id)
            serializers=EmployeeSerializer(employee_obj)
            return Response({'status':200,"payload":serializers.data})
        
    def update(self,request,pk):
        id=pk
        if id is not None:
            employee_obj=Employee.objects.get(id=id)
            serializers=EmployeeSerializer(instance=employee_obj,data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response({'status':200,"payload":serializers.data})
            else:
                return Response({'status':400,"payload":serializers.errors})
    def destroy(self,request,pk):
        id=pk
        if id is not None:
            employee_obj=Employee.objects.get(id=id)
            employee_obj.delete()
            return Response("Employee is deleted successfully")
        
    def create(self,request):
        serializers=EmployeeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'status':200,"payload":serializers.data})
        else:
            return Response({'status':400,"payload":serializers.errors})


#APIView decorator
@api_view(['GET'])
def home(request):
    employee_obj=Employee.objects.all()
    serializers=EmployeeSerializer(employee_obj,many=True)
    return Response({'status':200,"payload":serializers.data})

@api_view(['POST'])
def employe_post(request):
    employee_obj=Employee.objects.all()
    serializers=EmployeeSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response({'status':200,"payload":serializers.data})
    else:
        return Response({'status':400,"payload":serializers.errors})    
@api_view(['POST'])
def employe_update(request,id):
    employee_obj=Employee.objects.get(id=id)
    print(employee_obj,'2222222222')
    serializers=EmployeeSerializer(instance=employee_obj, data=request.data)
    print(serializers,'#222222###')
    if serializers.is_valid():
        serializers.save()
        return Response({'status':200,"payload":serializers.data})
    else:
        return Response({'status':400,"payload":serializers.errors})      
@api_view(['DELETE'])  
def employe_delete(request,id):
    employee_obj=Employee.objects.get(id=id)
    print(employee_obj,'2222222222')
    employee_obj.delete()
    return Response("Employee is deleted successfully")
@api_view(['DELETE'])  
def employe_delete(request,id):
    employee_obj=Employee.objects.get(id=id)
    print(employee_obj,'2222222222')
    employee_obj.delete()
    return Response("Employee is deleted successfully")     

# Mixin GenericAPIView
class Employee_list(ListModelMixin,GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    def get(self,request):
        return self.list(request)
    

class Employee_create(CreateModelMixin,GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    def post(self,request):
        return self.create(request) 

class Employee_retrieve(RetrieveModelMixin,GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    def get(self,request,**kwargs):
        return self.retrieve(request,**kwargs)     
      
class Employee_update(UpdateModelMixin,GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    def put(self,request,**kwargs):
        return self.update(request,**kwargs)  

class Employee_delete(DestroyModelMixin,GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    def delete(self,request,**kwargs):
        return self.destroy(request,**kwargs)


#concrete generic view
class employeelist(ListAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer

class employeecreate(CreateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
class employeeretrieve(RetrieveAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer    
class employeeupdate(UpdateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer   
class employeedelete(DestroyAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer 

class employeelistcreate(ListCreateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer    

class employeeretrieveupdate(RetrieveUpdateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer

class employeeretrievedelete(RetrieveDestroyAPIView):   
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer

class employeeretrieveupdatedestroy(RetrieveUpdateDestroyAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
