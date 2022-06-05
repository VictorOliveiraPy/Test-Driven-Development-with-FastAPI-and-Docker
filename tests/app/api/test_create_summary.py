import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestCreateSummary:
    def test_should_return_status_code_201(self, test_app_with_db):
        response = test_app_with_db.post(
            "/summaries/", data=json.dumps({"url": "https://foo.bar"})
        )

        assert response.status_code == 201

    def test_should_return_status_code_422(self, test_app):
        response = test_app.post("/summaries/", data=json.dumps({}))
        assert response.status_code == 422

    def test_should_return_invalid_json(self, test_app):
        response = test_app.post("/summaries/", data=json.dumps({}))
        assert response.json() == {
            "detail": [
                {
                    "loc": ["body", "url"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }

    def test_should_return_a_summary_when_passing_an_id(self, test_app_with_db):
        response = test_app_with_db.post(
            "/summaries/", data=json.dumps({"url": "https://foo.bar"})
        )
        summary_id = response.json()["id"]

        response = test_app_with_db.get(f"/summaries/{summary_id}/")
        response_dict = response.json()

        assert response_dict["id"] == summary_id
        assert response_dict["url"] == "https://foo.bar"
        assert response_dict["summary"]
        assert response_dict["created_at"]

    def test_read_summary_incorrect_id(self, test_app_with_db):
        response = test_app_with_db.get("/summaries/999/")
        assert response.status_code == 404
        assert response.json()["detail"] == "Summary not found"

        response = test_app_with_db.get("/summaries/0/")
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

    def test_read_all_summaries(self, test_app_with_db):
        response = test_app_with_db.post(
            "/summaries/", data=json.dumps({"url": "https://foo.bar"})
        )
        summary_id = response.json()["id"]

        response = test_app_with_db.get("/summaries/")
        assert response.status_code == 200

        response_list = response.json()
        assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1
