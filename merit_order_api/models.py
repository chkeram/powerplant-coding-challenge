from typing import List

from pydantic import BaseModel, Field


# TODO: add field_validator wrappers to validate values of various attributes (e.g. wind_percent, pmin/max etc)
class Fuels(BaseModel):
    gas_euro_per_mwh: float = Field(alias="gas(euro/MWh)")
    kerosine_euro_per_mwh: float = Field(alias="kerosine(euro/MWh)")
    co2_euro_per_ton: float = Field(alias="co2(euro/ton)")
    wind_percent: float = Field(alias="wind(%)")


class Powerplant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float


class PayloadModel(BaseModel):
    load: float
    fuels: Fuels
    powerplants: List[Powerplant]


class PowerplantSelection(BaseModel):
    name: str
    p: float
