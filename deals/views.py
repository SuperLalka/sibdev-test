import csv
import io

from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Deal, Gem
from .serializers import FileUploadSerializer, DealSerializer


class DealsViewSet(ModelViewSet):
    serializer_class = DealSerializer
    queryset = Deal.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            serializer_class = FileUploadSerializer
        else:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        best_buyers = Deal.objects.values('customer').annotate(
            spent_money=Sum('total')).order_by('-spent_money')[:5]
        serializer = self.get_serializer(best_buyers, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.initial_data['file']
        decoded_file = file.read().decode()
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)

        fieldnames = []
        for row in reader:
            if not fieldnames:
                fieldnames = row
                print(fieldnames)
                continue
            new_deal, created = Deal.objects.get_or_create(customer=User.objects.get_or_create(username=row[0])[0],
                                                           item=Gem.objects.get_or_create(name=row[1])[0],
                                                           total=row[2],
                                                           quantity=row[3],
                                                           date=row[4])
            if created:
                print(f'{row} has been entered into the database as {new_deal}')
            else:
                print(f'{row} already exists as {new_deal}')

        return Response("OK", status=status.HTTP_204_NO_CONTENT)
