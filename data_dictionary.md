# 📋 AgriShield AI: Core Data Dictionary

This document serves as the data dictionary for the core grounding datasets used in **AgriShield AI**.

---

## `data\weather.csv`

| Column Name | Data Type | Sample Value |
| :--- | :--- | :--- |
| `location` | String | `California Central Valley` |
| `date` | String | `2026-06-24` |
| `temperature_c` | Float | `38.2` |
| `humidity_pct` | Integer | `20` |
| `rainfall_mm` | Float | `0.0` |
| `climate_risk_level` | String | `High` |
| `forecast_summary` | String | `Extreme heatwave and severe drought conditions building over the basin.` |

---

## `data\crop.csv`

| Column Name | Data Type | Sample Value |
| :--- | :--- | :--- |
| `crop_type` | String | `Corn` |
| `ideal_soil` | String | `Loam` |
| `growth_stage` | String | `Vegetative` |
| `daily_water_requirement_liters` | Float | `5.5` |
| `baseline_yield_ton_per_acre` | Float | `4.5` |

---

## `data\disease.csv`

| Column Name | Data Type | Sample Value |
| :--- | :--- | :--- |
| `crop_type` | String | `Corn` |
| `disease_name` | String | `Northern Corn Leaf Blight` |
| `primary_symptoms` | String | `Long, elliptical, grayish-green lesions on leaves.` |
| `weather_trigger_condition` | String | `Moderate temperatures (18-27°C) with prolonged dampness.` |
| `prevention_protocol` | String | `Deploy resistant hybrids and optimize row crop spacing for aeration.` |

---

## `data\market.csv`

| Column Name | Data Type | Sample Value |
| :--- | :--- | :--- |
| `crop_type` | String | `Corn` |
| `current_price_per_ton` | Float | `195.5` |
| `demand_index` | Float | `0.78` |
| `market_region` | String | `Domestic Logistics Network` |
| `price_trend_forecast` | String | `Stable with mild upward pressure due to ethanol demand.` |

---