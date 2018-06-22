from django.urls import path

from .views import pages, APIs

urlpatterns = [
    path('', pages.index, name='index'),
    path('new', pages.index_new, name='index_new'),
    path('entity-recommendation/', APIs.entity_recommendation, name='entity-recommendation'),
    path('types/', APIs.find_types, name='types'),
    path('facts/', APIs.find_facts, name='facts'),
    path('attributes/', APIs.find_attributes, name='attributes'),
    path('one-row-direction/', APIs.find_one_row_direction, name='one-row-direction'),
    path('pattern/', APIs.find_pattern, name='pattern'),
    path('query-positive/', APIs.query_positive, name='query-positive'),
    path('strings/', APIs.find_strings, name='strings'), # deprecated
    path('query-negative/', APIs.query_negative, name='query-negative'), #deprecated
    path('query/', APIs.query, name='query'),
    path('get-more-results/', APIs.get_more_results, name='get_more_results'),
]
