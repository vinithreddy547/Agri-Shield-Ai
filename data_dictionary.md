# AgriShield AI Data Dictionary

This document serves as the data dictionary for the core datasets used in the **AgriShield AI: Climate Risk & Farm Decision Agent** project. These datasets support the Streamlit UI, risk assessments, and decision logic for agricultural risk mitigation.

---

## 1. Weather Dataset (`data/weather.csv`)
This dataset contains historical and current meteorological observations and regional climate risk forecasts.

### Schema
| Column Name | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `location` | String | The geographic region or agricultural hub. | `California Central Valley` |
| `date` | Date (YYYY-MM-DD) | The date of the weather record or forecast. | `2026-06-21` |
| `temperature_c` | Float | The recorded average daily temperature in Celsius (°C). | `38.2` |
| `humidity_pct` | Integer | The average relative humidity percentage (%). | `20` |
| `rainfall_mm` | Float | The daily precipitation measurement in millimeters (mm). | `0.0` |
| `climate_risk_level` | String | Evaluated risk categorization based on weather severity (`Low`, `Medium`, `High`). | `High` |
| `forecast_summary` | String | A brief narrative summary of the weather condition or specific alerts. | `Extreme heatwave and drought conditions` |

---

## 2. Crop Dataset (`data/crop.csv`)
This dataset maps crop characteristics, optimal growing environments, and baseline productivity benchmarks.

### Schema
| Column Name | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `crop_type` | String | The name or category of the crop. | `Corn` |
| `ideal_soil` | String | The target soil texture/type optimized for cultivation. | `Loam` |
| `growth_stage` | String | The current developmental phase of the crop. | `Vegetative` |
| `daily_water_requirement_liters` | Float | The recommended amount of water needed daily per unit/plant in liters. | `5.5` |
| `baseline_yield_ton_per_acre` | Float | Expected standard yield per acre under optimal conditions. | `4.5` |

---

## 3. Disease Dataset (`data/disease.csv`)
This dataset lists prevalent crop pathogens, symptomatic patterns, weather triggers, and mitigation practices.

### Schema
| Column Name | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `crop_type` | String | The crop susceptible to the disease (corresponds to `crop.csv`). | `Rice` |
| `disease_name` | String | The common name of the plant disease or pathogen. | `Rice Blast` |
| `primary_symptoms` | String | Visible signs of infection on the plant. | `Diamond-shaped lesions with grey centers` |
| `weather_trigger_condition` | String | Meteorological thresholds/conditions that catalyze disease outbreak. | `Cool temperatures (<25C) with high humidity` |
| `prevention_protocol` | String | Actionable guidelines to prevent or mitigate the disease spread. | `Planting resistant varieties and avoiding excess nitrogen` |

---

## 4. Market Dataset (`data/market.csv`)
This dataset tracks financial valuations, regional demand indicators, and trade outlooks for crop yields.

### Schema
| Column Name | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `crop_type` | String | The crop associated with market data (corresponds to `crop.csv`). | `Almonds` |
| `current_price_per_ton` | Float | The prevailing market price per metric ton in USD ($). | `4200.0` |
| `demand_index` | Float | A normalized demand metric (0.0 to 1.0) indicating buyer interest. | `0.90` |
| `market_region` | String | The primary distribution network or trading region. | `Global Export` |
| `price_trend_forecast` | String | Qualitative projection of the crop's market price movement. | `Increasing due to dry forecast in major growing regions` |
