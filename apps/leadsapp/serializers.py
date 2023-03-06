from rest_framework import serializers

from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

    def validate(self, data):
        if data['project'].user == self.context['request'].user:
            return data
        raise serializers.ValidationError('You are not allowed to create this lead')
