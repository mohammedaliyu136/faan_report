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
from .views import *

urlpatterns = [
    url(r'^monthly/report/$', report_json, name="monthly_report_json"),

    url(r'^data/(?P<time>\w+)/(?P<name>\w+)/$', report_json_final, name="monthly_report_json"),

    url(r'^(?P<time>\w+)/(?P<pk>\w+)/$', index, name='index'), #pk=value time
    url(r'^months/$', monthly_list, name='monthly_list'),
    url(r'^select/month/report/$', select_month_report, name='monthly_list'),
    url(r'^quater/$', quater, name='quater'),
    url(r'^annual/$', annual, name='annual'), #month/current/8/
    url(r'^hardcopy/(?P<time>\w+)/(?P<value>\w+)/(?P<pk>\w+)$', hardcopy, name='hardcopy'), #hardcopy/month/octobar/2
    url(r'^(?P<time>\w+)/(?P<name>\w+)/default/hardcopy/(?P<pk>\w+)/$', default_hardcopy, name='hardcopy'),
    url(r'^staff_list/report/dept/$', staff_list_report, name='staff_list_report'),
    url(r'^staff_list/$', staff_list_new, name='staff_list_new'),
    url(r'^staff/list/(?P<pk>\w+)/$', staff_list_detail_new, name='staff_list_new'),
    url(r'^audit/report/dept/$', audit, name='audit'),
    url(r'^audit_list/$', audit_staff_list_new, name='audit_staff_list_new'),
    url(r'^audit/list/(?P<pk>\w+)/$', audit_staff_list_detail_new, name='audit_staff_list_new'),
    url(r"^(?P<time>\w+)/(?P<name>\w+)/(?P<pk>\w+)/$", detail, name='detail'),


]

