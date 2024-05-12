## 📄 Documentation API


#### !! The path has a / icymelt / api / before use api

### 1. List all ice experiments

```
  GET /experiments/
```

---

### 2. Retrieve an ice experiment with a specific id

```
  GET /experiment/${id}
```

| Parameter | Type  | Description                                  |
| :-------- |:------|:---------------------------------------------|
| `id`      | `int` | Experiment id to retrieve with a specific id |

---

### 3. List all materials

```
  GET /materials/
```

---

### 4. Retrieve a material with a specific id

```
  GET /material/${id}
```

| Parameter | Type  | Description                                  |
| :-------- |:------|:---------------------------------------------|
| `id`      | `int` | Material id to retrieve with a specific id   |

---

### 5. List all weather conditions

```
  GET /weather-conditions/
```

---

### 6. Retrieve a weather condition with a specific id

```
  GET /weather-condition/${id}
```

| Parameter | Type  | Description                                          |
| :-------- |:------|:-----------------------------------------------------|
| `id`      | `int` | Weather condition id to retrieve with a specific id  |

---

### 7. List all ice experiments with a specific material id

```
  GET /experiment/material/${id}
```

| Parameter | Type  | Description                                      |
| :-------- |:------|:-------------------------------------------------|
| `id`      | `int` | Material id to retrieve with a specific material |

---

### 8. List all ice experiments with a specific weather condition id

```
  GET /experiment/weather-condition/${id}
```

| Parameter | Type  | Description                                          |
| :-------- |:------|:-----------------------------------------------------|
| `id`      | `int` | Weather condition id to retrieve with a specific id  |

---

### 9. List all ice experiments with a specific material id and weather condition id

```
  GET /experiment/material/${material_id}/weather-condition/${weather_condition_id}
```

| Parameter              | Type  | Description                                          |
|:-----------------------|:------|:-----------------------------------------------------|
| `material_id`          | `int` | Material id to retrieve with a specific material     |
| `weather_condition_id` | `int` | Weather condition id to retrieve with a specific id  |

---

### 10. Get average values for all measurements

```
  GET /averageAllMeasurements/
```

---

### 11. Get total values for all measurements

```
  GET /totalAllMeasurements/
```

---

### 12. Get minimum values for all measurements

```
  GET /minAllMeasurements/
```

---

### 13. Get maximum values for all measurements

```
  GET /maxAllMeasurements/
```

---

### 14. Get statistical values for all measurements

```
  GET /statisticalAllMeasurements/
```

---