"""ems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import employee, department, designation, employee_list, employee_create, employee_detail, get_emp, employee_edit, employee_editt

urlpatterns = [
    url(r'^$', employee, name='employee'),
    url(r'^list$', employee_list, name='employee'), 
    #url(r"^detail/(?P<pk>\w+)/$", employee_detail, name='detail'),
    url(r"^edit/(?P<pk>\w+)/$", employee_edit, name='employee_edit'),
    url(r"^create/$", employee_create, name='employee_edit'),
    url(r'^departments$', department, name='department'),
    url(r'^designations$', designation, name='designation'),
    url(r"^(?P<action>\w+)/(?P<pk>\w+)/$", employee_editt, name='employee_editt'),



    url(r'^emp/(?P<pk>\w+)/$', get_emp, name='get_emp'),

]

