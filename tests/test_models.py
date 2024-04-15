import unittest
import json

from pydantic import ValidationError

from merit_order_api.models import PayloadModel, Fuels, Powerplant, PowerplantSelection

fuel_payload_json = {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 0
}


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

    def test_wind_percent_valid(self):
        wind_values = [0, 50, 100]

        for wind_value in wind_values:
            with self.subTest(wind=wind_value):
                fuel_payload_json["wind(%)"] = wind_value
                fuels = Fuels(**fuel_payload_json)
                self.assertEqual(fuels.wind_percent, wind_value)

    def test_wind_percent_invalid(self):
        """ Test with invalid wind percentages """
        wind_values = [-1, 101]
        for wind_value in wind_values:
            fuel_payload_json["wind(%)"] = wind_value
            with self.subTest(wind=wind_value):
                with self.assertRaises(ValueError):
                    Fuels(**fuel_payload_json)

