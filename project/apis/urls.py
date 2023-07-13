"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import *
from apis import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee', views.employeeviewset, basename='employee')

router = DefaultRouter()
router.register('employeemodal', views.employeemodalviewset, basename='employee')

router = DefaultRouter()
router.register('employeehyper', views.employeehyperviewset, basename='employee')

urlpatterns = [
    #api view decorator
    path('', home),
    path('add/', employe_post),
    path('update/<int:id>', employe_update),
    path('delete/<int:id>', employe_delete),

    #generic api view
    path('list/', views.Employee_list.as_view()),
    path('retrieve/<int:pk>/', views.Employee_retrieve.as_view()),
    path('update_mixin/<int:pk>/', views.Employee_update.as_view()),
    path('destroy/<int:pk>/', views.Employee_delete.as_view()),


    #concrete api view
    path('api_list/', views.employeelist.as_view()),
    path('api_create/', views.employeecreate.as_view()),
    path('api_retrieve/<int:pk>/', views.employeeretrieve.as_view()),
    path('api_update/<int:pk>/', views.employeeupdate.as_view()),
    path('api_delete/<int:pk>/', views.employeedelete.as_view()),
    path('api_list_create/', views.employeelistcreate.as_view()),
    path('api_retrive_update/<int:pk>/', views.employeeretrieveupdate.as_view()),
    path('api_retrive_delete/<int:pk>/', views.employeeretrievedelete.as_view()),
    path('api_retrive_update_delete/<int:pk>/', views.employeeretrieveupdatedestroy.as_view()),

    #viewset
    path('api/',include(router.urls)),

    #modal viewset
    path('modalapi/',include(router.urls)),
    #in modal viewset LOGINS
    path('auth/',include('rest_framework.urls', namespace='rest_framework.urls')),
    # hyper viewset i t will come hyperlink for id
    path('hyperapi/',include(router.urls)),

]

# http://127.0.0.1:8000/modalapi/employeemodal/19
#http://127.0.0.1:8000/admin/
# http://127.0.0.1:8000/api/employee/19

#http://127.0.0.1:8000/hyperapi/employeehyper/19
# {
#         "url": "http://127.0.0.1:8000/hyperapi/employeehyper/16/",
#         "emp_id": "60001",
#         "name": "Soora Saikrishna",
#         "month": "Jul-23",
#         "pf_status": "Yes",
#         "gross": "700000.00",
#         "net_days": 8,
#         "arrears": "0.00",
#         "shift_allowance": "0.00"
#     },