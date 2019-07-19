"""site_myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from pages.views import home_view, gen_to_brand_view, brand_to_gen_view, results_strength_view , results_price_view, brand_to_generic_result_view

urlpatterns = [

    path('admin/', admin.site.urls),
    path('home/', home_view , name = 'home_view'),

    path('generic2brand/', gen_to_brand_view, name='gen_to_brand_view'),
    path('brand2generic/', brand_to_gen_view, name='brand_to_gen_view'),
    #path('signup/',signup_view , name='signup_page'),
    #path('login/',login_view , name='login_page'),

    path('brand2genericName',brand_to_generic_result_view,name='brand_to_generic_result_view'),
    path('strengths_options/', results_strength_view, name='results_strength_view'),
    path('price_options/', results_price_view, name='results_price_view')
]
