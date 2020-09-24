import pytest
from invenio_nusl_theses.proxies import nusl_theses


@pytest.mark.usefixtures("app", "db", "taxonomy_tree", "base_json", "base_json_dereferenced")
class TestRecord:
    def test_canonical_url(self, app, db, base_json_dereferenced):
        record = nusl_theses.create_draft_record(base_json_dereferenced)
        with app.app_context():
            assert record.canonical_url == "http://127.0.0.1:5000/theses/411100"
