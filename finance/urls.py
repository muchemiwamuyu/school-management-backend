from django.urls import path
from .views import *

urlpatterns = [
    path('stk-push/', stk_push, name='stk-push'),

]