import json


class TestCreateSummary:
    def test_should_return_status_code_201(self, test_app_with_db):
        response = test_app_with_db.post("/summaries/", data=json.dumps({"url": "https://foo.bar"}))

        assert response.status_code == 201

    def test_should_return_status_code_422(self, test_app):
        response = test_app.post("/summaries/", data=json.dumps({}))
        assert response.status_code == 422

    def test_should_return_invalid_json(self, test_app):
        response = test_app.post("/summaries/", data=json.dumps({}))
        assert response.json() == {
            'detail': [{'loc': ['body', 'url'], 'msg': 'field required', 'type': 'value_error.missing'},
                       {'loc': ['body', 'id'], 'msg': 'field required', 'type': 'value_error.missing'}]}

    def test_should_return_a_summary_when_passing_an_id(self, test_app_with_db):
        response = test_app_with_db.post("/summaries/", data=json.dumps({"url": "https://foo.bar"}))
        summary_id = response.json()["id"]

        response = test_app_with_db.get(f"/summaries/{summary_id}/")
        response_dict = response.json()

        assert response_dict["id"] == summary_id
        assert response_dict["url"] == "https://foo.bar"
        assert response_dict["summary"]
        assert response_dict["created_at"]
