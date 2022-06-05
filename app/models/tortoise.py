from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class TextSummary(models.Model):
    url: str = fields.TextField()
    summary: str = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url


SummarySchema = pydantic_model_creator(TextSummary)
