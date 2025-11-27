from rest_framework.generics import ListAPIView
from .models import Developer
from .serializers import DeveloperSerializer

class DeveloperListAPIView(ListAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
