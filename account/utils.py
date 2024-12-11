from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, Http404):
            return Response({
                'error': 'Not found',
                'detail': str(exc)
            }, status=status.HTTP_404_NOT_FOUND)
        
        if isinstance(exc, ValidationError):
            return Response({
                'error': 'Validation Error',
                'detail': exc.messages
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'error': 'Internal Server Error',
            'detail': str(exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response 