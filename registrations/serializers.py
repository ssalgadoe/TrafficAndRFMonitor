from .models import Customers
from rest_framework import serializers



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('name', 'lon_id','lat_id')


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('name', 'lon_id','lat_id')