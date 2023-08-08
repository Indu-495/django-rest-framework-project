import io
import os
from django.shortcuts import render
from django.shortcuts import render
import pandas as pd
import requests
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveDestroyAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication,SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import FileResponse, HttpResponse, JsonResponse, StreamingHttpResponse
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import CallReportMaster
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
User = get_user_model()

class Command(BaseCommand):
    help = 'Create tokens for all existing users.'

    def handle(self, *args, **options):
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS('Successfully created tokens for all users.'))


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'password': user.password
        })

class EmployeeUpdateView(UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'emp_id'  # Field to use for lookup instead of the default 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        (print(request.data,'*************************'))
        return self.update(request, *args, **kwargs)


def upload_file_html(request):
    if request.method == 'POST':
        url = 'http://127.0.0.1:8000/upload_file/'  # API endpoint URL
        files = {'profiles': request.FILES['profiles']}  # Assuming 'profiles' is the key for the uploaded file

        response = requests.post(url, files=files)
        if response.status_code == 201:
            return render(request, 'success.html')
        else:
            error_message = f"Error: {response.status_code}"
            return render(request, 'error.html', {'error_message': error_message})
    else:
        return render(request, 'upload.html')


class EmployeeUploadView(APIView):
    def post(self, request, format=None):
        # Check if the 'profiles' key exists in the request.FILES dictionary
        print(request.FILES,'22222222222222222222222')
        if 'profiles' not in request.FILES:
            return Response({"error": "File 'profiles' is missing in the request."}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['profiles']
        df = pd.read_csv(file)

        for _, row in df.iterrows():
            employee_data = {
                'emp_id': row[0],
                'name': row[1],
                'month': row[2],
                'pf_status': row[3],
                'gross': row[4],
                'net_days': row[5],
                'arrears': row[6],
                'shift_allowance': row[7],
            }
            serializer = EmployeeSerializer(data=employee_data)
            if serializer.is_valid():
                serializer.save()
            else:
                # If any row data is invalid, return the errors with a bad request response
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'File uploaded and data saved successfully.'}, status=status.HTTP_201_CREATED)

def create_html(request):
    if request.method == 'POST':
        form_data = {
            'emp_id': request.POST.get('emp_id'),
            'name': request.POST.get('name'),
            'month': request.POST.get('month'),
            'pf_status': request.POST.get('pf_status'),
            'gross': request.POST.get('gross'),
            'net_days': request.POST.get('net_days'),
            'arrears': request.POST.get('arrears'),
            'shift_allowance': request.POST.get('shift_allowance')
        }

        api_url = request.build_absolute_uri('/create/')
        response = requests.post(api_url, data=form_data)

        if response.ok:
            return render(request, 'create.html')
        else:
            error_message = 'An error occurred while creating the employee.'
            return render(request, 'error.html', {'message': error_message})
        a==b

    return render(request, 'create.html')

def list_html(request):
    return render(request,'list.html')

def generate_excel_html(request):
    if request.method == 'POST':
        # Get the values from the HTML form
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        # Make a POST request to the generate_excel API endpoint
        response = requests.post('http://127.0.0.1:8000/generate_excel/', data={
            'from_date': from_date,
            'to_date': to_date
        })

        # Check if the request was successful
        if response.status_code == 200:
            # Get the file content from the response
            file_content = response.content
            file_name = response.headers['Content-Disposition'].split('=')[1].replace('"', '')

            # Define the directory where you want to save the Excel file
            save_directory = 'C:/INDU/django_project/'

            # Create the file path by joining the directory and file name
            file_path = os.path.join(save_directory, file_name)

            # Write the file content to the specified file path
            with open(file_path, 'wb') as file:
                file.write(file_content)

            # TODO: Process the response as needed
            # For example, you can save the Excel file or display a success message
            return HttpResponse(f'Excel file generated successfully. File name: {file_name}, File path: {file_path}')
        else:
            # Handle the case where the request was not successful
            # You can display an error message or redirect to an error page
            return HttpResponse('Error: Unable to generate the Excel file.')
    else:
        # Render the HTML template
        return render(request, 'template.html')

@api_view(['POST'])
def generate_excel(request):
    if request.method == 'POST':
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')

        # Retrieve data from the database
        data = CallReportMaster.objects.filter(date__range=(from_date, to_date)).values(
            'sno', 'emp_id', 'ref_type', 'unique_id', 'name', 'design', 'contact', 'camp', 'camp_details',
            'date', 'time', 'location', 'latitude', 'longitude', 'area', 'city', 'state', 'pincode',
            'district', 'station', 'branch', 'source', 'attendance', 'reason', 'type', 'ldate', 'category', 'status'
        )

        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Generate the file name
        file_name = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"

        # Create a BytesIO buffer
        buffer = io.BytesIO()

        # Write the DataFrame to the Excel file in the buffer
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Seek to the beginning of the buffer
        buffer.seek(0)

        # Create a streaming response with the buffer data
        response = StreamingHttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response

    return Response({'status': 400})
class employeehyperviewset(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=employeehyperserializer

#model viewset based one class we do all crud operations 
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
        return Response({'status':"Success","payload":serializers.data})
    else:
        return Response({'status':"Bad Request","payload":serializers.errors})    
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

# Mixin GenericAPIView
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class Employee_list(ListModelMixin,GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    def get(self,request):
        return self.list(request)
    

class Employee_create(CreateModelMixin,GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    def post(self,request):
        print(type(request.data))
        print(request.data,'@@@@@@@@@@@')
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

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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