from django.db.models import Count
from django_filters.rest_framework import FilterSet, BooleanFilter
from .models import Document

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DocumentFilter(FilterSet):
    seq_annotations__isnull = BooleanFilter(field_name='seq_annotations', method='filter_annotations')
    doc_annotations__isnull = BooleanFilter(field_name='doc_annotations', method='filter_annotations')
    seq2seq_annotations__isnull = BooleanFilter(field_name='seq2seq_annotations', method='filter_annotations')

    def filter_annotations(self, queryset, field_name, value):
        queryset = queryset.annotate(num_annotations=Count(field_name))

        should_have_annotations = not value
        if should_have_annotations:
            queryset = queryset.filter(num_annotations__gte=1)
        else:
            queryset = queryset.filter(num_annotations__lte=0)

        return queryset

    class Meta:
        model = Document
        fields = ('project', 'text', 'meta', 'created_at', 'updated_at',
                  'doc_annotations__label__id', 'seq_annotations__label__id',
                  'doc_annotations__isnull', 'seq_annotations__isnull', 'seq2seq_annotations__isnull')
