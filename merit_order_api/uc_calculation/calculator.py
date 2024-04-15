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


def merit_order_calculator(measurements: PayloadModel) -> List[PowerplantSelection]:
    print("measurements------\n", measurements)
    logger.info(measurements)
    return mock_response

