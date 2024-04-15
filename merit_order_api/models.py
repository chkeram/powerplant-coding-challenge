from typing import List
from enum import Enum

from pydantic import BaseModel, Field, field_validator, validator


class PoweplantType(Enum):
    gasfired = "gasfired"
    turbojet = "turbojet"
    windturbine = "windturbine"


# TODO: add field_validator wrappers to validate values of various attributes (e.g. wind_percent, pmin/max etc)
class Fuels(BaseModel):
    gas_euro_per_mwh: float = Field(alias="gas(euro/MWh)")
    kerosine_euro_per_mwh: float = Field(alias="kerosine(euro/MWh)")
    co2_euro_per_ton: float = Field(alias="co2(euro/ton)")
    wind_percent: float = Field(alias="wind(%)")

    @field_validator('wind_percent', mode='before')
    def check_wind_percentage(cls, v):
        if not (0 <= v <= 100):
            raise ValueError('Wind percentage must be between 0 and 100')
        return v


class Powerplant(BaseModel):
    name: str
    type: PoweplantType
    efficiency: float
    pmin: float
    pmax: float

    @field_validator('efficiency', mode='before')
    def check_efficiency(cls, v):
        if not (0 <= v <= 100):
            raise ValueError('efficiency must be between 0 and 100')
        return v

    @field_validator('pmin', 'pmax', mode='before')
    def chck_pmax_pmax(cls, v):
        if not (0 <= v):
            raise ValueError('Pimax and Pmin cannot be a negative number')
        return v

    class Config:
        use_enum_values = True


class PayloadModel(BaseModel):
    load: float
    fuels: Fuels
    powerplants: List[Powerplant]


class PowerplantSelection(BaseModel):
    name: str
    p: float
