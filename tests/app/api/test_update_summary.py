import json


class TestUpdateSummary:
    def test_update_summary(self, test_app_with_db):
        response = test_app_with_db.post(
            "/summaries/", data=json.dumps({"url": "https://foo.bar"})
        )
        summary_id = response.json()["id"]

        response = test_app_with_db.put(
            f"/summaries/{summary_id}/",
            data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
        )
        assert response.status_code == 200

        response_dict = response.json()
        assert response_dict["id"] == summary_id
        assert response_dict["url"] == "https://foo.bar"
        assert response_dict["summary"] == "updated!"
        assert response_dict["created_at"]

    def test_update_summary_incorrect_id(self, test_app_with_db):
        response = test_app_with_db.put(
            "/summaries/999/",
            data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Summary not found"

        response = test_app_with_db.put(
            f"/summaries/0/",
            data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["path", "id"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ]
        }

    def test_update_summary_invalid_json(self, test_app_with_db):
        response = test_app_with_db.post(
            "/summaries/", data=json.dumps({"url": "https://foo.bar"})
        )
        summary_id = response.json()["id"]

        response = test_app_with_db.put(
            f"/summaries/{summary_id}/", data=json.dumps({})
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["body", "url"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "summary"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }

    def test_update_summary_invalid_keys(self, test_app_with_db):
        response = test_app_with_db.post(
            "/summaries/", data=json.dumps({"url": "https://foo.bar"})
        )
        summary_id = response.json()["id"]

        response = test_app_with_db.put(
            f"/summaries/{summary_id}/", data=json.dumps({"url": "https://foo.bar"})
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["body", "summary"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }

        response = test_app_with_db.put(
            f"/summaries/{summary_id}/",
            data=json.dumps({"url": "invalid://url", "summary": "updated!"}),
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
