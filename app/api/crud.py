from typing import List, Union

from app.api.ping import router
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import TextSummary


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(
        url=payload.url,
        summary="dummy summary",
    )
    await summary.save()
    return summary.id


async def get(id: int) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).first().values()
    if summary:
        return summary

    return None


async def get_all() -> List:
    summaries = await TextSummary.all().values()
    return summaries
