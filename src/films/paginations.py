#films/paginations.pys
from rest_framework import pagination
from rest_framework.response import Response


class MyFormatResultsSetPagination(pagination.PageNumberPagination):

    page_size_query_param = "page_size"
    page_query_param = 'page'
    page_size = 10
    max_page_size = 1000

    """
    define pagation
    """
    def get_paginated_response(self, data):
        """
        setting return context format
        """
        return Response({
            'results': data,
            'pagination': self.page.paginator.count,
            'page_size': self.page.paginator.per_page,
            'page': self.page.start_index() // self.page.paginator.per_page + 1
        })