from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_page_size(self, request):
        if 'HTTP_PAGINATION' in request.META:
            return request.META['HTTP_PAGINATION']
