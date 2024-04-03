from rest_framework.pagination import PageNumberPagination

__all__ = []


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 1000
