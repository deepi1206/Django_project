from . import views
from django.urls import path


urlpatterns = [
        path('',views.login_view,name='login'),
        path('signup',views.signup_view,name='signup'),
        path('expense',views.expense,name='home'),
        path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    ]