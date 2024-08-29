# accounts/serializers.py
from . models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'dob', 'password' ]
        
    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super(UserSerializer, self).__init__(*args, **kwargs)
        
        # Determine the context (signup or login)
        context = self.context.get('action')
        
        # If it's a login, remove unnecessary fields
        if context == 'login':
            self.fields.pop('dob')
            self.fields.pop('phone_number')


    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            dob=validated_data['dob'],
            phone_number=validated_data['phone_number']
        )
        return user
