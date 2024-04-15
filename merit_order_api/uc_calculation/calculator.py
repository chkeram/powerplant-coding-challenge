import logging
from typing import List

from merit_order_api.models import PayloadModel, PowerplantSelection

logger = logging.getLogger(__name__)


example_response = [
    {
        "name": "windpark1",
        "p": 90.0
    },
    {
        "name": "windpark2",
        "p": 21.6
    },
    {
        "name": "gasfiredbig1",
        "p": 460.0
    },
    {
        "name": "gasfiredbig2",
        "p": 338.4
    },
    {
        "name": "gasfiredsomewhatsmaller",
        "p": 0.0
    },
    {
        "name": "tj1",
        "p": 0.0
    }
]

mock_response = []
for i in example_response:
    mock_response.append(PowerplantSelection(**i))


# Function to calculate the production plan
def calculate_production_plan(payload: PayloadModel):
    # Extract data from the payload
    load = payload.load
    fuels = payload.fuels
    powerplants = payload.powerplants

    # Calculate cost per MWh for each plant and sort by cost
    plant_costs = []
    for plant in powerplants:
        if plant.type == 'windturbine':
            # Wind turbines' cost is effectively zero and output depends on wind availability
            cost_per_mwh = 0
            possible_output = plant.pmax * (fuels.wind_percent / 100)
        else:
            if plant.type == 'gasfired':
                fuel_cost = fuels.gas_euro_per_mwh
            elif plant.type == 'turbojet':
                fuel_cost = fuels.kerosine_euro_per_mwh
            cost_per_mwh = fuel_cost / plant.efficiency
            if plant.type == 'gasfired':
                cost_per_mwh += fuels.co2_euro_per_ton / 1000  # Assuming emission is per MWh
            possible_output = plant.pmax

        plant_costs.append({
            'name': plant.name,
            'cost': cost_per_mwh,
            'max_output': possible_output,
            'min_output': plant.pmin
        })

    # Sort plants by cost
    plant_costs.sort(key=lambda x: x['cost'])

    # Calculate the production plan
    production_plan = []
    total_generated = 0

    for plant in plant_costs:
        if total_generated >= load:
            break
        max_possible = min(plant['max_output'], load - total_generated)
        if max_possible >= plant['min_output']:
            power_generated = max_possible
            total_generated += power_generated
            production_plan.append(PowerplantSelection(name=plant['name'], p=power_generated))

    return production_plan


# remove v1
# add validators
# unittest for calculator

