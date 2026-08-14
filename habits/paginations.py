from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 5  # количество записей на страницу
    page_size_query_param = (
        "page_size"  # при передаче данного параметра можно указать нужно количество записей на страницу
    )
    max_page_size = 10  # Максимальное количество записей на одну страницу
