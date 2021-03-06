"""BusinessHRMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include
from core.api import urls as core_urls
from businesscard.api import urls as card_urls
from employees.api import urls as emp_urls
from management import urls as mgmt_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/', include(core_urls)),
    path('api/v1/bussinesscard/', include(card_urls)),
    path('api/v1/employees/', include(emp_urls)),
    path('adminpanel/', include(mgmt_urls)),

]
