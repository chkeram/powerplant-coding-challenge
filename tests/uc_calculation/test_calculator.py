import unittest
import json
import os
from pydantic import ValidationError
from merit_order_api.models import Powerplant, PowerplantSelection, PayloadModel
from merit_order_api.uc_calculation.calculator import calculate_production_plan


current_dir = os.getcwd()
relative_path = '../example_payload_response/payload.json'
example_payload_path = os.path.abspath(os.path.join(current_dir, relative_path))


class TestCalculatorl(unittest.TestCase):

    def test_valid_payload_from_json(self):
        with open(example_payload_path, "r") as f:
            payload_json = json.load(f)

        payload = PayloadModel(**payload_json)
        expected_load = payload.load

        output = calculate_production_plan(payload=payload)

        calculated_load = 0
        for plant in output:
            calculated_load += plant.p
        self.assertEqual(expected_load, calculated_load)
