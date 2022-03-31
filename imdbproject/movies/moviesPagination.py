from rest_framework.pagination import PageNumberPagination

class MoviesListPagination(PageNumberPagination):
    page_size = 10
