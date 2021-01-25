import collections

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Deal, Gem


class BestBuyersSerializer(serializers.Serializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        best_buyers_gems = collections.defaultdict(list)

        for gem in Gem.objects.all():
            gem_buyers = Deal.objects.filter(item=gem).values_list('customer', flat=True).distinct()
            buyers_intersection = set(gem_buyers).intersection(set([item['customer'] for item in self.instance]))
            if len(buyers_intersection) > 1:
                [best_buyers_gems[buyer].append(gem.name) for buyer in buyers_intersection]

        representation['username'] = User.objects.get(id=instance['customer']).username
        representation['spent_money'] = instance['spent_money']
        representation['gems'] = best_buyers_gems[instance['customer']]
        return representation
