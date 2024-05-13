from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import IceExp, Material, WeatherCondition
from django.db.models import Avg, Sum, Min, Max
from rest_framework.exceptions import ErrorDetail


class APITestWithData(TestCase):
    def setUp(self):
        self.weather_cond1 = WeatherCondition.objects.create(code=200, weather="test_weather_cond")
        self.weather_cond2 = WeatherCondition.objects.create(code=201, weather="test_weather_cond2")

        self.material1 = Material.objects.create(type="test_material")
        self.material2 = Material.objects.create(type="test_material2")

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

    def test_ice_exp_detail(self):
        url = reverse('icymelt:ice_exp_detail_api', kwargs={'id': self.ice_exp.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "id": self.ice_exp.id,
            "temp": "28.00",
            "humidity": "79.00",
            "thickness": "2.10",
            "weight": "9.40",
            "duration": "905.00",
            "weather_cond": self.ice_exp.weather_cond.id,
            "material": self.ice_exp.material.id
        }
        del response.data["date"]
        self.assertEqual(response.data, expected_data)


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

    def test_material_detail(self):
        url = reverse('icymelt:material_detail_api', kwargs={'id': self.ice_exp.material.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "id": self.ice_exp.material.id,
            "type": "test_material"
        }
        self.assertEqual(response.data, expected_data)

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

        for material_id, averages in response.data['average'].items():
            material_id = int(material_id)
            material = Material.objects.get(pk=material_id)

            self.assertEqual(averages['material_id'], material.id)
            self.assertEqual(averages['material_type'], material.type)
            self.assertEqual(averages['record_count'], IceExp.objects.filter(material=material).count())

            expected_avg_temp = IceExp.objects.filter(material=material).aggregate(avg_temp=Avg('temp'))['avg_temp']
            expected_avg_humidity = IceExp.objects.filter(material=material).aggregate(avg_humidity=Avg('humidity'))[
                'avg_humidity']
            expected_avg_thickness = IceExp.objects.filter(material=material).aggregate(avg_thickness=Avg('thickness'))[
                'avg_thickness']
            expected_avg_weight = IceExp.objects.filter(material=material).aggregate(avg_weight=Avg('weight'))[
                'avg_weight']
            expected_avg_duration = IceExp.objects.filter(material=material).aggregate(avg_duration=Avg('duration'))[
                'avg_duration']

            self.assertAlmostEqual(averages['temp'], expected_avg_temp, places=2)
            self.assertAlmostEqual(averages['humidity'], expected_avg_humidity, places=2)
            self.assertAlmostEqual(averages['thickness'], expected_avg_thickness, places=2)
            self.assertAlmostEqual(averages['weight'], expected_avg_weight, places=2)
            self.assertAlmostEqual(averages['duration'], expected_avg_duration, places=2)

    def test_total_all_measurements(self):
        url = reverse('icymelt:total_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for material_id, totals in response.data['total'].items():
            material_id = int(material_id)
            material = Material.objects.get(pk=material_id)

            self.assertEqual(totals['material_id'], material.id)
            self.assertEqual(totals['material_type'], material.type)
            self.assertEqual(totals['record_count'], IceExp.objects.filter(material=material).count())

            expected_total_temp = IceExp.objects.filter(material=material).aggregate(total_temp=Sum('temp'))['total_temp']
            expected_total_humidity = IceExp.objects.filter(material=material).aggregate(total_humidity=Sum('humidity'))['total_humidity']
            expected_total_thickness = IceExp.objects.filter(material=material).aggregate(total_thickness=Sum('thickness'))['total_thickness']
            expected_total_weight = IceExp.objects.filter(material=material).aggregate(total_weight=Sum('weight'))['total_weight']
            expected_total_duration = IceExp.objects.filter(material=material).aggregate(total_duration=Sum('duration'))['total_duration']

            self.assertAlmostEqual(totals['temp'], expected_total_temp, places=2)
            self.assertAlmostEqual(totals['humidity'], expected_total_humidity, places=2)
            self.assertAlmostEqual(totals['thickness'], expected_total_thickness, places=2)
            self.assertAlmostEqual(totals['weight'], expected_total_weight, places=2)
            self.assertAlmostEqual(totals['duration'], expected_total_duration, places=2)

    def test_min_all_measurements(self):
        url = reverse('icymelt:min_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for material_id, mins in response.data['min'].items():
            material_id = int(material_id)
            material = Material.objects.get(pk=material_id)

            self.assertEqual(mins['material_id'], material.id)
            self.assertEqual(mins['material_type'], material.type)
            self.assertEqual(mins['record_count'], IceExp.objects.filter(material=material).count())

            expected_min_temp = IceExp.objects.filter(material=material).aggregate(min_temp=Min('temp'))['min_temp']
            expected_min_humidity = IceExp.objects.filter(material=material).aggregate(min_humidity=Min('humidity'))[
                'min_humidity']
            expected_min_thickness = IceExp.objects.filter(material=material).aggregate(min_thickness=Min('thickness'))[
                'min_thickness']
            expected_min_weight = IceExp.objects.filter(material=material).aggregate(min_weight=Min('weight'))[
                'min_weight']
            expected_min_duration = IceExp.objects.filter(material=material).aggregate(min_duration=Min('duration'))[
                'min_duration']

            self.assertAlmostEqual(mins['temp'], expected_min_temp, places=2)
            self.assertAlmostEqual(mins['humidity'], expected_min_humidity, places=2)
            self.assertAlmostEqual(mins['thickness'], expected_min_thickness, places=2)
            self.assertAlmostEqual(mins['weight'], expected_min_weight, places=2)
            self.assertAlmostEqual(mins['duration'], expected_min_duration, places=2)

    def test_max_all_measurements(self):
        url = reverse('icymelt:max_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for material_id, maxs in response.data['max'].items():
            material_id = int(material_id)
            material = Material.objects.get(pk=material_id)

            self.assertEqual(maxs['material_id'], material.id)
            self.assertEqual(maxs['material_type'], material.type)
            self.assertEqual(maxs['record_count'], IceExp.objects.filter(material=material).count())

            expected_max_temp = IceExp.objects.filter(material=material).aggregate(max_temp=Max('temp'))['max_temp']
            expected_max_humidity = IceExp.objects.filter(material=material).aggregate(max_humidity=Max('humidity'))[
                'max_humidity']
            expected_max_thickness = IceExp.objects.filter(material=material).aggregate(max_thickness=Max('thickness'))[
                'max_thickness']
            expected_max_weight = IceExp.objects.filter(material=material).aggregate(max_weight=Max('weight'))[
                'max_weight']
            expected_max_duration = IceExp.objects.filter(material=material).aggregate(max_duration=Max('duration'))[
                'max_duration']

            self.assertAlmostEqual(maxs['temp'], expected_max_temp, places=2)
            self.assertAlmostEqual(maxs['humidity'], expected_max_humidity, places=2)
            self.assertAlmostEqual(maxs['thickness'], expected_max_thickness, places=2)
            self.assertAlmostEqual(maxs['weight'], expected_max_weight, places=2)
            self.assertAlmostEqual(maxs['duration'], expected_max_duration, places=2)

    def test_statistical_all_measurements(self):
        url = reverse('icymelt:statistical_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for material_id, stats in response.data.items():
            material_id = int(material_id)
            material = Material.objects.get(pk=material_id)

            self.assertEqual(stats['material_id'], material.id)
            self.assertEqual(stats['material_type'], material.type)
            self.assertEqual(stats['record_count'], IceExp.objects.filter(material=material).count())

            expected_avg_temp = IceExp.objects.filter(material=material).aggregate(avg_temp=Avg('temp'))['avg_temp']
            expected_min_temp = IceExp.objects.filter(material=material).aggregate(min_temp=Min('temp'))['min_temp']
            expected_max_temp = IceExp.objects.filter(material=material).aggregate(max_temp=Max('temp'))['max_temp']
            expected_total_temp = IceExp.objects.filter(material=material).aggregate(total_temp=Sum('temp'))[
                'total_temp']

            expected_avg_humidity = IceExp.objects.filter(material=material).aggregate(avg_humidity=Avg('humidity'))[
                'avg_humidity']
            expected_min_humidity = IceExp.objects.filter(material=material).aggregate(min_humidity=Min('humidity'))[
                'min_humidity']
            expected_max_humidity = IceExp.objects.filter(material=material).aggregate(max_humidity=Max('humidity'))[
                'max_humidity']
            expected_total_humidity = \
            IceExp.objects.filter(material=material).aggregate(total_humidity=Sum('humidity'))['total_humidity']

            expected_avg_thickness = IceExp.objects.filter(material=material).aggregate(avg_thickness=Avg('thickness'))[
                'avg_thickness']
            expected_min_thickness = IceExp.objects.filter(material=material).aggregate(min_thickness=Min('thickness'))[
                'min_thickness']
            expected_max_thickness = IceExp.objects.filter(material=material).aggregate(max_thickness=Max('thickness'))[
                'max_thickness']
            expected_total_thickness = \
            IceExp.objects.filter(material=material).aggregate(total_thickness=Sum('thickness'))['total_thickness']

            expected_avg_weight = IceExp.objects.filter(material=material).aggregate(avg_weight=Avg('weight'))[
                'avg_weight']
            expected_min_weight = IceExp.objects.filter(material=material).aggregate(min_weight=Min('weight'))[
                'min_weight']
            expected_max_weight = IceExp.objects.filter(material=material).aggregate(max_weight=Max('weight'))[
                'max_weight']
            expected_total_weight = IceExp.objects.filter(material=material).aggregate(total_weight=Sum('weight'))[
                'total_weight']

            expected_avg_duration = IceExp.objects.filter(material=material).aggregate(avg_duration=Avg('duration'))[
                'avg_duration']
            expected_min_duration = IceExp.objects.filter(material=material).aggregate(min_duration=Min('duration'))[
                'min_duration']
            expected_max_duration = IceExp.objects.filter(material=material).aggregate(max_duration=Max('duration'))[
                'max_duration']
            expected_total_duration = \
            IceExp.objects.filter(material=material).aggregate(total_duration=Sum('duration'))['total_duration']

            self.assertAlmostEqual(stats['temp']['mean'], expected_avg_temp, places=2)
            self.assertAlmostEqual(stats['temp']['min'], expected_min_temp, places=2)
            self.assertAlmostEqual(stats['temp']['max'], expected_max_temp, places=2)
            self.assertAlmostEqual(stats['temp']['total'], expected_total_temp, places=2)

            self.assertAlmostEqual(stats['humidity']['mean'], expected_avg_humidity, places=2)
            self.assertAlmostEqual(stats['humidity']['min'], expected_min_humidity, places=2)
            self.assertAlmostEqual(stats['humidity']['max'], expected_max_humidity, places=2)
            self.assertAlmostEqual(stats['humidity']['total'], expected_total_humidity, places=2)

            self.assertAlmostEqual(stats['thickness']['mean'], expected_avg_thickness, places=2)
            self.assertAlmostEqual(stats['thickness']['min'], expected_min_thickness, places=2)
            self.assertAlmostEqual(stats['thickness']['max'], expected_max_thickness, places=2)
            self.assertAlmostEqual(stats['thickness']['total'], expected_total_thickness, places=2)

            self.assertAlmostEqual(stats['weight']['mean'], expected_avg_weight, places=2)
            self.assertAlmostEqual(stats['weight']['min'], expected_min_weight, places=2)
            self.assertAlmostEqual(stats['weight']['max'], expected_max_weight, places=2)
            self.assertAlmostEqual(stats['weight']['total'], expected_total_weight, places=2)

            self.assertAlmostEqual(stats['duration']['mean'], expected_avg_duration, places=2)
            self.assertAlmostEqual(stats['duration']['min'], expected_min_duration, places=2)
            self.assertAlmostEqual(stats['duration']['max'], expected_max_duration, places=2)
            self.assertAlmostEqual(stats['duration']['total'], expected_total_duration, places=2)


class APITestNoData(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_ice_exp_list_no_data(self):
        url = reverse('icymelt:ice_exp_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_ice_exp_detail_no_data(self):
        url = reverse('icymelt:ice_exp_detail_api', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='No IceExp matches the given query.', code='not_found')})

    def test_ice_exp_by_material_no_data(self):
        url = reverse('icymelt:experiment_by_material_api', kwargs={'mat_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_ice_exp_by_weather_condition_no_data(self):
        url = reverse('icymelt:experiment_by_weather_condition_api', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_ice_exp_by_material_and_weather_condition_no_data(self):
        url = reverse('icymelt:experiment_by_material_and_weather_condition_api', kwargs={'mat_id': 1, 'wea_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_material_list_no_data(self):
        url = reverse('icymelt:material_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_material_detail_no_data(self):
        url = reverse('icymelt:material_detail_api', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='No Material matches the given query.', code='not_found')})

    def test_weather_condition_list_no_data(self):
        url = reverse('icymelt:weather_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_weather_condition_detail_no_data(self):
        url = reverse('icymelt:weather_condition_detail_api', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='No WeatherCondition matches the given query.', code='not_found')})

    def test_average_all_measurements_no_data(self):
        url = reverse('icymelt:average_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'average': {}})

    def test_total_all_measurements_no_data(self):
        url = reverse('icymelt:total_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'total': {}})

    def test_min_all_measurements_no_data(self):
        url = reverse('icymelt:min_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'min': {}})

    def test_max_all_measurements_no_data(self):
        url = reverse('icymelt:max_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'max': {}})

    def test_statistical_all_measurements_no_data(self):
        url = reverse('icymelt:statistical_all_measurements_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

