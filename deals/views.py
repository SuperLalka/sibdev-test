import csv
import io
import logging

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Deal, Gem
from .serializers import FileUploadSerializer, BestBuyersSerializer


logger = logging.getLogger(__name__)


class DealsViewAPI(APIView):

    def get(self, request):
        best_buyers = (Deal.objects.values('customer')
                           .annotate(spent_money=Sum('total'))
                           .order_by('-spent_money')[:5])
        serializer = BestBuyersSerializer(best_buyers, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        try:
            serializer = FileUploadSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            file = serializer.initial_data['file']
            decoded_file = file.read().decode()
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string)

            fieldnames = []
            for row in reader:
                if not fieldnames:
                    fieldnames = row
                    continue

                customer, _ = User.objects.get_or_create(username=row[0])
                item, _ = Gem.objects.get_or_create(name=row[1])

                new_deal, created = Deal.objects.get_or_create(
                    customer=customer, item=item, total=row[2], quantity=row[3], date=row[4]
                )

                if created:
                    logger.info(f'{row} has been entered into the database as {new_deal}')
                else:
                    logger.info(f'{row} already exists as {new_deal}')

            return Response("OK", status=status.HTTP_204_NO_CONTENT)
        except ValidationError:
            return Response("Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
