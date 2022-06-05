import json


class TestRemoveSummary:
    def test_remove_summary(self, test_app_with_db):
        response = test_app_with_db.post(
            "/summaries/", data=json.dumps({"url": "https://foo.bar"})
        )
        summary_id = response.json()["id"]

        response = test_app_with_db.delete(f"/summaries/{summary_id}/")
        assert response.status_code == 200
        assert response.json() == {"id": summary_id, "url": "https://foo.bar"}

    def test_remove_summary_incorrect_id(self, test_app_with_db):
        response = test_app_with_db.delete("/summaries/999/")
        assert response.status_code == 404
        assert response.json()["detail"] == "Summary not found"

        response = test_app_with_db.delete("/summaries/0/")
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
