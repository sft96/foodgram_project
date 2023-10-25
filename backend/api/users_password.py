from rest_framework.decorators import api_view
from rest_framework.response import Response
import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import (CharField,
                                        Serializer,
                                        ValidationError)


class UserPasswordSerializer(Serializer):
    new_password = CharField(
        label='New Password'
    )
    current_password = CharField(
        label='Current Password'
    )

    def validate_current_password(self, current_password):
        user = self.context['request'].user
        if not authenticate(
                username=user.email,
                password=current_password
        ):
            raise ValidationError(
                'Unable to sign in with the provided credentials.',
                code='authorization'
            )
        return current_password

    def validate_new_password(self, new_password):
        validators.validate_password(new_password)
        return new_password

    def create(self, validated_data):
        user = self.context['request'].user
        password = make_password(
            validated_data.get('new_password')
        )
        user.password = password
        user.save()
        return validated_data


@api_view(['post'])
def set_password(request):
    """Change password"""
    serializer = UserPasswordSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'The password has already been changed!'
        })
    return Response({
        'error': 'Enter correct data!'
    })
