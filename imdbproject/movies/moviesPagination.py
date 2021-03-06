from itertools import count
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MoviesListPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):

        return Response({ 
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'currentPage': self.page.number
    })

class CommentListPagination(PageNumberPagination):
    page_size = 3
    