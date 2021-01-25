import csv
import io
import logging

from django.contrib.auth.models import User
from django.db.models import Sum
from memoize import memoize, delete_memoized
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Deal, Gem
from .serializers import BestBuyersSerializer

logger = logging.getLogger(__name__)


class DealsViewAPI(APIView):

    def get(self, request):
        return Response(self._extract_users_list())

    @staticmethod
    @memoize(timeout=60 * 15)
    def _extract_users_list():
        best_buyers = (
            Deal.objects.values('customer')
                .annotate(spent_money=Sum('total'))
                .order_by('-spent_money')[:5]
        )
        return BestBuyersSerializer(best_buyers, many=True).data

    def post(self, request):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']
        decoded_file = file.read().decode()
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)

        next(reader)
        for row in reader:
            try:
                customer, _ = User.objects.get_or_create(username=row[0])
                item, _ = Gem.objects.get_or_create(name=row[1])

                new_deal, created = Deal.objects.get_or_create(
                    customer=customer, item=item, total=row[2], quantity=row[3], date=row[4]
                )

                if created:
                    logger.info(f'{row} has been entered into the database as {new_deal}')
                else:
                    logger.info(f'{row} already exists as {new_deal}')
            except LookupError:
                return Response("Error", status=status.HTTP_400_BAD_REQUEST)
            finally:
                delete_memoized(self._extract_users_list)

        return Response("OK", status=status.HTTP_204_NO_CONTENT)
