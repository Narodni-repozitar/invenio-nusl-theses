# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from invenio_records_rest.utils import allow_all, deny_all
from oarepo_communities.links import community_record_links_factory
from oarepo_records_draft import DRAFT_IMPORTANT_FILTERS
from oarepo_records_draft.rest import DRAFT_IMPORTANT_FACETS

from nr_common.config import FACETS, CURATOR_FACETS, CURATOR_FILTERS, FILTERS
from nr_theses.record import draft_index_name
from oarepo_multilingual import language_aware_text_term_facet, language_aware_text_terms_filter
from oarepo_ui.facets import translate_facets, term_facet
from oarepo_ui.filters import boolean_filter

from nr_theses.search import ThesisRecordsSearch

_ = lambda x: x

RECORDS_DRAFT_ENDPOINTS = {
    'theses': {
        'draft': 'draft-theses',
        'pid_type': 'nrthe',
        'pid_minter': 'nr_theses',
        'pid_fetcher': 'nr_theses',
        'default_endpoint_prefix': True,
        'max_result_window': 500000,
        'record_class': 'nr_theses.record:PublishedThesisRecord',
        'list_route': '/<community_id>/theses/',
        'item_route': f'/<commpid(nrthe,model="theses",record_class="nr_theses.record:PublishedThesisRecord"):pid_value>',

        'publish_permission_factory_imp': 'nr_theses.permissions.publish_draft_object_permission_impl',
        'unpublish_permission_factory_imp': 'nr_theses.permissions.unpublish_draft_object_permission_impl',
        'edit_permission_factory_imp': 'nr_theses.permissions.update_object_permission_impl',
        'list_permission_factory_imp': allow_all,
        'read_permission_factory_imp': allow_all,
        'create_permission_factory_imp': deny_all,
        'update_permission_factory_imp': deny_all,
        'delete_permission_factory_imp': deny_all,
        'default_media_type': 'application/json',
        'links_factory_imp': community_record_links_factory,
        'search_class': ThesisRecordsSearch,
        # 'indexer_class': CommitingRecordIndexer,
        'files': dict(
            # Who can upload attachments to a draft dataset record
            put_file_factory=deny_all,
            # Who can download attachments from a draft dataset record
            get_file_factory=allow_all,
            # Who can delete attachments from a draft dataset record
            delete_file_factory=deny_all
        )

    },
    'draft-theses': {
        'pid_type': 'dnrthe',
        'record_class': 'nr_theses.record:DraftThesisRecord',
        'list_route': '/<community_id>/theses/draft/',
        'item_route': f'/<commpid(nrthe,model="theses/draft",record_class="nr_theses.record:DraftThesisRecord"):pid_value>',
        'search_index': draft_index_name,
        'links_factory_imp': community_record_links_factory,
        'search_class': ThesisRecordsSearch,
'search_serializers': {
            'application/json': 'oarepo_validate:json_search',
        },
        'record_serializers': {
            'application/json': 'oarepo_validate:json_response',
        },

        'create_permission_factory_imp': 'nr_theses.permissions.create_draft_object_permission_impl',
        'update_permission_factory_imp': 'nr_theses.permissions.update_draft_object_permission_impl',
        'read_permission_factory_imp': 'nr_theses.permissions.read_draft_object_permission_impl',
        'delete_permission_factory_imp': 'nr_theses.permissions.delete_draft_object_permission_impl',
        'list_permission_factory_imp': 'nr_theses.permissions.list_draft_object_permission_impl',
        'record_loaders': {
            'application/json': 'oarepo_validate.json_files_loader',
            'application/json-patch+json': 'oarepo_validate.json_loader'
        },
        'files': dict(
            put_file_factory='nr_theses.permissions.put_draft_file_permission_impl',
            get_file_factory='nr_theses.permissions.get_draft_file_permission_impl',
            delete_file_factory='nr_theses.permissions.delete_draft_file_permission_impl'
        )
    }
}

THESES_FILTERS = {
    _('defended'): boolean_filter('defended'),
    _('studyField'): language_aware_text_terms_filter('studyField.title', suffix=".keyword"),
    _('degreeGrantor'): language_aware_text_terms_filter('degreeGrantor.title', suffix=".keyword"),
    #     _('person'): terms_filter('person.keyword'),
    #     _('accessRights'): group_by_terms_filter('accessRights.title.en.raw', {
    #         "true": "open access",
    #         1: "open access",
    #         True: "open access",
    #         "1": "open access",
    #         False: ["embargoed access", "restricted access", "metadata only access"],
    #         0: ["embargoed access", "restricted access", "metadata only access"],
    #         "false": ["embargoed access", "restricted access", "metadata only access"],
    #         "0": ["embargoed access", "restricted access", "metadata only access"],
    #     }),
    #     _('resourceType'): language_aware_text_terms_filter('resourceType.title'),
    #     _('keywords'): language_aware_text_terms_filter('keywords'),
    #     _('subject'): language_aware_text_terms_filter('subjectAll'),
    #     _('language'): language_aware_text_terms_filter('language.title'),
    #     _('date'): range_filter('dateAll.date'),
    #     _('dateIssued'): range_filter('dateIssued.date'),
    #     _('dateDefended'): range_filter('dateDefended.date'),
    #     _('dateModified'): range_filter('dateModified.date'),
    #
}
#
# CURATOR_FILTERS = {
#     _('rights'): language_aware_text_terms_filter('rights.title'),
#     _('provider'): language_aware_text_terms_filter('provider.title'),
#     _('isGL'): boolean_filter('isGL')
# }
#
THESES_FACETS = {
    'defended': term_facet('defended'),
    'studyField': language_aware_text_term_facet('studyField.title', suffix=".keyword"),
    'degreeGrantor': language_aware_text_term_facet('degreeGrantor.title', suffix=".keyword"),
    # 'person': term_facet('person.keyword'),
    # 'accessRights': term_facet('accessRights.title.en.raw'),
    # 'resourceType': language_aware_text_term_facet('resourceType.title'),
    # 'keywords': language_aware_text_term_facet('keywords'),
    # 'subject': language_aware_text_term_facet('subjectAll'),
    # 'language': language_aware_text_term_facet('language.title'),
    # 'date': date_histogram_facet('dateAll.date'),
}
#
# CURATOR_FACETS = {
#     'rights': language_aware_text_term_facet('rights.title'),
#     'provider': language_aware_text_term_facet('provider.title'),
#     'dateIssued': date_histogram_facet('dateIssued.date'),
#     'dateDefended': date_histogram_facet('dateDefended.date'),
#     'dateModified': date_histogram_facet('dateModified.date'),
#     'isGL': term_facet('isGL'),
# }

RECORDS_REST_FACETS = {
    draft_index_name: {
        "aggs": translate_facets({**THESES_FACETS, **FACETS, **CURATOR_FACETS, **DRAFT_IMPORTANT_FACETS},
                                 label='{facet_key}',
                                 value='{value_key}'),
        "filters": {**THESES_FILTERS, **FILTERS, **CURATOR_FILTERS, **DRAFT_IMPORTANT_FILTERS}
    },
}

RECORDS_REST_SORT_OPTIONS = {
    draft_index_name: {
        'alphabetical': {
            'title': 'alphabetical',
            'fields': [
                'title.cs.raw'
            ],
            'default_order': 'asc',
            'order': 1
        },
        'best_match': {
            'title': 'Best match',
            'fields': ['_score'],
            'default_order': 'desc',
            'order': 1,
        }
    }
}

RECORDS_REST_DEFAULT_SORT = {
    draft_index_name: {
        'query': 'best_match',
        'noquery': 'best_match'
    }
}
