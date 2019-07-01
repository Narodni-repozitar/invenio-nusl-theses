# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for CIS theses repository."""

from __future__ import absolute_import, print_function

from flask import Blueprint
from invenio_explicit_acls.utils import convert_relative_schema_to_absolute
from marshmallow import ValidationError

from invenio_nusl_theses.api import ThesisAPI, ThesisRecord
from invenio_nusl_theses.marshmallow import ThesisMetadataSchemaV1
from invenio_nusl_theses.proxies import nusl_theses
from . import config


class InvenioNUSLTheses(object):
    """CIS theses repository extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        from invenio_records.signals import before_record_update, before_record_insert
        self.init_config(app)
        app.extensions['invenio-nusl-theses'] = ThesisAPI(app)
        before_record_update.connect(validate_thesis)
        before_record_insert.connect(validate_thesis)

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """

        app.config.setdefault('RECORDS_REST_ENDPOINTS', {}).update(getattr(config, 'RECORDS_REST_ENDPOINTS'))

        app.config.setdefault('RECORDS_REST_FACETS', {}).update(config.RECORDS_REST_FACETS)

        app.config.setdefault('RECORDS_REST_SORT_OPTIONS', {}).update(config.RECORDS_REST_SORT_OPTIONS)

        app.config.setdefault('RECORDS_REST_DEFAULT_SORT', {}).update(config.RECORDS_REST_DEFAULT_SORT)


def validate_thesis(*args, record=None, **kwargs):
    if not isinstance(record, ThesisRecord):
        return
    schema = record._convert_and_get_schema(record)
    if schema != convert_relative_schema_to_absolute(ThesisRecord.STAGING_SCHEMA):
        return
    marshmallow_schema = ThesisMetadataSchemaV1(strict=True)
    try:
        nusl_theses.validate(marshmallow_schema, record,
                             "https://nusl.cz/schemas/invenio_nusl_theses/nusl-theses-v1.0.0.json")
        record["validations"] = {
            "valid": True
        }

    except ValidationError as e:
        record["validations"] = {
            "valid": False
        }
        # TODO: do extra přihodit fieldy, které jsou špatně
        # for field in e.field_names:
        #     error_counts[field] += 1
        #     error_documents[field].append(recid)
        # if set(e.field_names) - IGNORED_ERROR_FIELDS:
        #     raise
        # continue