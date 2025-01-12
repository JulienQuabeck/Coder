from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import baseInfoSerializer
from market_app.models import BaseInfo
from django.http import JsonResponse

# Create your views here.
class baseInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = BaseInfo.objects.all()
        serializer = baseInfoSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)