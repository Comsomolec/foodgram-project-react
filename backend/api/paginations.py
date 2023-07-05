from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Пагинация с параметром limit."""
    page_size_query_param = 'limit'
