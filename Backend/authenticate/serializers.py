from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SadhanaEntry

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        
    def create(self, validated_data):
        """Override create method to hash password before saving"""
        user = User(
            username = validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password']) #hash password
        user.save()
        return user
    
class SadhanaEntrySerializer(serializers.ModelSerializer):
    wake_up_time = serializers.TimeField(format='%H:%M')

    # Custom method to return `card_filled_at` in HH:MM format
    card_filled_at = serializers.SerializerMethodField() # custom time format HH : MM

    def get_card_filled_at(self, obj):
        if obj.card_filled_at:
            return obj.card_filled_at.strftime('%H:%M')  # Format as HH:MM
        return None
    
    class Meta:
        model = SadhanaEntry
        fields = '__all__'