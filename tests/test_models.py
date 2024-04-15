import unittest
import json

from pydantic import ValidationError

from merit_order_api.models import PayloadModel, Fuels, Powerplant, PowerplantSelection

# TODO: unittests of api route calls (mocked) + functional tests


class TestPayloadModel(unittest.TestCase):

    def test_valid_payload_from_json(self):
        with open("example_payload_response/payload.json", "r") as f:
            payload_json = json.load(f)

        payload = PayloadModel(**payload_json)

        self.assertEqual(payload.load, 910)
        self.assertEqual(payload.fuels.gas_euro_per_mwh, 13.4)
        self.assertEqual(payload.fuels.kerosine_euro_per_mwh, 50.8)
        self.assertEqual(payload.fuels.co2_euro_per_ton, 20)
        self.assertEqual(payload.fuels.wind_percent, 60)
        self.assertEqual(len(payload.powerplants), 6)

    def test_valid_response_from_json(self):
        with open("example_payload_response/response.json", "r") as f:
            response_json = json.load(f)

        response = []
        for i in response_json:
            response.append(PowerplantSelection(**i))

        expected_first_selection = {
                "name": "windpark1",
                "p": 90.0
        }
        self.assertEqual(response[0].p, expected_first_selection['p'])
        self.assertEqual(response[0].name, expected_first_selection['name'])
        self.assertEqual(len(response), 6)

    def test_invalid_response(self):
        with self.assertRaises(ValidationError):
            PowerplantSelection(
                selection=[
                    {
                        "name": "windpark1",
                        "p": "90.0"
                    }
                ]
            )



