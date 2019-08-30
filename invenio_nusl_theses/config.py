# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from elasticsearch_dsl import Q
from invenio_records_rest.facets import terms_filter
from invenio_records_rest.utils import deny_all, check_elasticsearch, allow_all
from invenio_search import RecordsSearch

from invenio_nusl_theses.api import ThesisSearch
from invenio_nusl_theses.marshmallow import ThesisRecordSchemaV1, ThesisMetadataSchemaV1
from invenio_nusl_theses.record import PublishedThesisRecord, DraftThesisRecord

THESES_SEARCH_INDEX = 'invenio_nusl_theses-nusl-theses-v1.0.0'
THESES_STAGING_SEARCH_INDEX = 'invenio_nusl_theses-nusl-theses-staging-v1.0.0'
THESES_PID = 'pid(nusl,record_class="invenio_nusl_theses.api:ThesisRecord")'
THESES_STAGING_JSON_SCHEMA = "https://nusl.cz/schemas/invenio_nusl_theses/nusl-theses-staging-v1.0.0.json"

DRAFT_ENABLED_RECORDS_REST_ENDPOINTS = {
    'theses': {
        'json_schemas': [
            'invenio_nusl_theses/nusl-theses-v1.0.0.json'
        ],
        'published_pid_type': 'nusl',
        'pid_minter': 'nusl',
        'pid_fetcher': 'nusl',
        'draft_pid_type': 'dnusl',
        'draft_allow_patch': True,

        'record_marshmallow': ThesisRecordSchemaV1,
        'metadata_marshmallow': ThesisMetadataSchemaV1,

        'draft_record_class': DraftThesisRecord,
        'published_record_class': PublishedThesisRecord,

        'publish_permission_factory': allow_all,
        'unpublish_permission_factory': allow_all,
        'edit_permission_factory': allow_all,

        # 'search_class': DebugACLRecordsSearch,
        # 'indexer_class': CommitingRecordIndexer,

    }
}

INVENIO_OAREPO_UI_COLLECTIONS = {
    "theses": {
        "title": {
            "cs-cz": "Vysokoškolské práce",
            "en-us": "Theses"
        },
        "description": {
            "cs-cz": """

""",
            "en-us": """

"""
        },
        "rest": "/api/drafts/theses/",
        "facet_filters": list()
    },
}

INVENIO_RECORD_DRAFT_SCHEMAS = [
    'invenio_nusl_theses/nusl-theses-v1.0.0.json',
]


def nested_terms_filter(prefix, field, field_query=None):
    """Create a term filter.

    :param field: Field name.
    :returns: Function that returns the Terms query.
    """

    field = prefix + '.' + field

    def inner(values):
        if field_query:
            query = field_query(field)(values)
        else:
            query = Q('terms', **{field: values})
        return Q('nested', path=prefix, query=query)

    return inner


def year_filter(field):
    """Create a term filter.

    :param field: Field name.
    :returns: Function that returns the Terms query.
    """

    def inner(values):
        queries = []
        for value in values:
            queries.append(
                Q('range', **{
                    field: {
                        "gte": value,
                        "lt": int(value) + 1,
                        "format": "yyyy"
                    }
                })
            )
        return Q('bool', should=queries, minimum_should_match=1)

    return inner


FILTERS = {
    'yearAccepted': year_filter('dateAccepted'),
    'language': terms_filter('language'),
    'defended': terms_filter('defended'),
    'doctype.slug': terms_filter('doctype.slug'),
    'person.keyword': terms_filter('person.keyword'),
    'subjectKeywords': terms_filter('subjectKeywords'),
    'accessRights': terms_filter('accessRights')
    # 'stylePeriod.title.value.keyword': terms_filter('stylePeriod.title.value.keyword'),
    # 'itemType.title.value.keyword': terms_filter('itemType.title.value.keyword'),
    # 'parts.material.materialType.title.value.keyword':
    #     nested_terms_filter('parts', 'material.materialType.title.value.keyword'),
    # 'parts.material.fabricationTechnology.title.value.keyword':
    #     nested_terms_filter('parts', 'material.fabricationTechnology.title.value.keyword'),
    # 'parts.material.color.title.value.keyword':
    #     nested_terms_filter('parts', 'material.color.title.value.keyword'),
    # 'parts.restorationMethods.title.value.keyword':
    #     nested_terms_filter('parts', 'restorationMethods.title.value.keyword'),
}

RECORDS_REST_FACETS = {
    'draft-invenio_nusl_theses-nusl-theses-v1.0.0': {
        'aggs': {  # agregace
            'yearAccepted': {
                "date_histogram": {
                    "field": "dateAccepted",
                    "interval": "1y",
                    "format": "yyyy",
                    "min_doc_count": 1,
                    "order": {
                        "_key": "desc"
                    }

                }
            },
            'language': {
                'terms': {
                    'field': 'language',
                    'size': 10
                }
            },
            'defended': {
                'terms': {
                    'field': 'defended'
                }
            },
            'doctype.slug': {
                'terms': {
                    'field': 'doctype.slug'
                }
            },
            'person': {
                'terms': {
                    'field': 'person.keyword'
                }
            },
            'subjectKeywords': {
                'terms': {
                    'field': 'subjectKeywords'
                }
            },
            'accessRights': {
                'terms': {
                    'field': 'accessRights'
                }
            },
            # 'degreeGrantor': {
            #     'nested': {
            #
            #     }
            # }
            # 'restorationRequestor.title.value.keyword': {
            #     'terms': {
            #       'field': 'restorationRequestor.title.value.keyword',
            #       'size': 100,
            #       "order": {"_term": "asc"}}},
            # 'stylePeriod.title.value.keyword': {
            #     'terms': {
            #       'field': 'stylePeriod.title.value.keyword',
            #       'size': 100,
            #       "order": {"_term": "desc"}}},
            # 'itemType.title.value.keyword': {
            #     'terms': {
            #       'field': 'itemType.title.value.keyword',
            #       'size': 100,
            #       "order": {"_term": "desc"}}},
            # 'parts': {  # if nested
            #     "nested": {
            #         "path": "parts"
            #     },
            #     "aggs": {
            #         "parts.materialType.title.value.keyword": {
            #             'terms': {'field': 'parts.materialType.title.value.keyword', 'size': 100,
            #                       "order": {"_term": "desc"}}
            #         },
            #         "parts.fabricationTechnology.title.value.keyword": {
            #             'terms': {'field': 'parts.fabricationTechnology.title.value.keyword', 'size': 100,
            #                       "order": {"_term": "desc"}}
            #         },
            #         "parts.color.title.value.keyword": {
            #             'terms': {'field': 'parts.color.title.value.keyword', 'size': 100,
            #                       "order": {"_term": "desc"}}
            #         },
            #         "parts.restorationMethods.title.value.keyword": {
            #             'terms': {'field': 'parts.restorationMethods.title.value.keyword', 'size': 100,
            #                       "order": {"_term": "desc"}}
            #         }
            #     }
            # },
        },
        'filters': FILTERS
    }
}

RECORDS_REST_SORT_OPTIONS = {
}

RECORDS_REST_DEFAULT_SORT = {
}
