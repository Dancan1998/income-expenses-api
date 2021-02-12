from django.urls import path
from .views import IncomeListAPIView, IncomeDetailAPIView

app_name = 'income'

urlpatterns = [
    path('', IncomeListAPIView.as_view(), name="income-list"),
    path('<int:id>', IncomeDetailAPIView.as_view(), name="income-detils"),
]
