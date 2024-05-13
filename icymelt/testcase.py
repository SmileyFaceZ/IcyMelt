from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import IceExp, Material, WeatherCondition


class APITestCase(TestCase):
    def setUp(self):
        # Create WeatherCondition objects
        self.weather_cond1 = WeatherCondition.objects.create(code=200, weather="test_weather_cond")
        self.weather_cond2 = WeatherCondition.objects.create(code=201, weather="test_weather_cond2")

        # Create Material objects
        self.material1 = Material.objects.create(type="test_material")
        self.material2 = Material.objects.create(type="test_material2")

        # Create IceExp objects
        self.ice_exp_data = {
            "temp": "28.00",
            "humidity": "79.00",
            "thickness": "2.10",
            "weight": "9.40",
            "duration": "905.00",
            "weather_cond": self.weather_cond1,
            "material": self.material1
        }
        self.ice_exp = IceExp.objects.create(**self.ice_exp_data)

        self.ice_exp_data2 = {
            "temp": "30.00",
            "humidity": "80.00",
            "thickness": "2.20",
            "weight": "9.50",
            "duration": "915.00",
            "weather_cond": self.weather_cond1,
            "material": self.material1
        }
        self.ice_exp2 = IceExp.objects.create(**self.ice_exp_data2)

        self.client = APIClient()

    def test_ice_exp_list(self):
        url = reverse('icymelt:ice_exp_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [{
            "id": self.ice_exp.id,
            "temp": "28.00",
            "humidity": "79.00",
            "thickness": "2.10",
            "weight": "9.40",
            "duration": "905.00",
            "weather_cond": self.ice_exp.weather_cond.id,
            "material": self.ice_exp.material.id
        }, {
            "id": self.ice_exp2.id,
            "temp": "30.00",
            "humidity": "80.00",
            "thickness": "2.20",
            "weight": "9.50",
            "duration": "915.00",
            "weather_cond": self.ice_exp.weather_cond.id,
            "material": self.ice_exp.material.id
        }]
        for i in range(len(response.data)):
            del response.data[i]["date"]
            self.assertEqual(response.data[i], expected_data[i])

    # Add expected data for test_ice_exp_by_material
    def test_ice_exp_by_material(self):
        url = reverse('icymelt:experiment_by_material_api', kwargs={'mat_id': self.ice_exp.material.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [{
            "id": self.ice_exp.id,
            "temp": "28.00",
            "humidity": "79.00",
            "thickness": "2.10",
            "weight": "9.40",
            "duration": "905.00",
            "weather_cond": self.ice_exp.weather_cond.id,
            "material": self.ice_exp.material.id
        }, {
            "id": self.ice_exp2.id,
            "temp": "30.00",
            "humidity": "80.00",
            "thickness": "2.20",
            "weight": "9.50",
            "duration": "915.00",
            "weather_cond": self.ice_exp.weather_cond.id,
            "material": self.ice_exp.material.id
        }]
        for i in range(len(response.data)):
            del response.data[i]["date"]
            self.assertEqual(response.data[i], expected_data[i])

    # Add expected data for test_ice_exp_by_weather_condition
    def test_ice_exp_by_weather_condition(self):
        url = reverse('icymelt:experiment_by_weather_condition_api', kwargs={'id': self.ice_exp.weather_cond.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [{
            "id": self.ice_exp.id,
            "temp": "28.00",
            "humidity": "79.00",
            "thickness": "2.10",
            "weight": "9.40",
            "duration": "905.00",
            "weather_cond": self.ice_exp.weather_cond.id,
            "material": self.ice_exp.material.id
        },{
            "id": self.ice_exp2.id,
            "temp": "30.00",
            "humidity": "80.00",
            "thickness": "2.20",
            "weight": "9.50",
            "duration": "915.00",
            "weather_cond": self.ice_exp.weather_cond.id,
            "material": self.ice_exp.material.id
        }]
        for i in range(len(response.data)):
            del response.data[i]["date"]
            self.assertEqual(response.data[i], expected_data[i])

    # Add expected data for test_ice_exp_by_material_and_weather_condition
    def test_ice_exp_by_material_and_weather_condition(self):
        url = reverse('icymelt:experiment_by_material_and_weather_condition_api',
                      kwargs={'mat_id': self.ice_exp.material.id, 'wea_id': self.ice_exp.weather_cond.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [{
            "id": self.ice_exp.id,
            "temp": "28.00",
            "humidity": "79.00",
            "thickness": "2.10",
            "weight": "9.40",
            "duration": "905.00",
            "weather_cond": self.ice_exp.weather_cond.id,
            "material": self.ice_exp.material.id
        }, {
            "id": self.ice_exp2.id,
            "temp": "30.00",
            "humidity": "80.00",
            "thickness": "2.20",
            "weight": "9.50",
            "duration": "915.00",
            "weather_cond": self.ice_exp.weather_cond.id,
            "material": self.ice_exp.material.id
        }]
        for i in range(len(response.data)):
            del response.data[i]["date"]
            self.assertEqual(response.data[i], expected_data[i])

    # Add expected data for test_material_list
    def test_material_list(self):
        url = reverse('icymelt:material_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [{
            "id": self.material1.id,
            "type": "test_material"
        },{
            "id": self.material2.id,
            "type": "test_material2"
        }]
        self.assertEqual(response.data, expected_data)

    # Add expected data for test_material_detail
    def test_material_detail(self):
        url = reverse('icymelt:material_detail_api', kwargs={'id': self.ice_exp.material.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "id": self.ice_exp.material.id,
            "type": "test_material"
        }
        self.assertEqual(response.data, expected_data)

    # Add expected data for test_weather_condition_list
    def test_weather_condition_list(self):
        url = reverse('icymelt:weather_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [{
            "id": self.weather_cond1.id,
            "code": 200,
            "weather": "test_weather_cond"
        },{
            "id": self.weather_cond2.id,
            "code": 201,
            "weather": "test_weather_cond2"
        }]
        self.assertEqual(response.data, expected_data)

    # Add expected data for test_weather_condition_detail
    def test_weather_condition_detail(self):
        url = reverse('icymelt:weather_condition_detail_api', kwargs={'id': self.ice_exp.weather_cond.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "id": self.ice_exp.weather_cond.id,
            "code": 200,
            "weather": "test_weather_cond"
        }
        self.assertEqual(response.data, expected_data)

    def test_average_all_measurements(self):
        url = reverse('icymelt:average_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_total_all_measurements(self):
        url = reverse('icymelt:total_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_min_all_measurements(self):
        url = reverse('icymelt:min_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_max_all_measurements(self):
        url = reverse('icymelt:max_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statistical_all_measurements(self):
        url = reverse('icymelt:statistical_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)