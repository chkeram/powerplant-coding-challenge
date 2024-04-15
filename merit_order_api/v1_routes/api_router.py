import logging
from typing import List

from pydantic import BaseModel, Field, conint, validator
from fastapi import APIRouter, HTTPException, Depends, Query, Request

from merit_order_api.models import PayloadModel, PowerplantSelection
from merit_order_api.uc_calculation.calculator import calculate_production_plan

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/merit-order", status_code=201, response_model=List[PowerplantSelection])
def merit_order_request(payload: PayloadModel):
    return calculate_production_plan(payload=payload)
