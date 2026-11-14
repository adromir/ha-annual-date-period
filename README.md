# 📅 Annual Date Period Helper for Home Assistant

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=adromir&repository=ha-annual-date-period&category=integration)
[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/adromir)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/default)
[![GitHub Release](https://img.shields.io/github/v/release/adromir/ha-annual-date-period?style=for-the-badge&color=blue)](https://github.com/adromir/ha-annual-date-period/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/adromir/ha-annual-date-period)

A lightweight, native **Home Assistant Helper Integration** that allows creating recurring, year-independent annual date periods (e.g., heating season, summer pool mode, holiday illumination, or vacation seasons) directly through the Home Assistant UI.

Exposes clean `binary_sensor` entities that turn `on` when today's date falls within the configured period, automatically re-evaluates at midnight, and provides rich countdown attributes.

---

## ✨ Key Features & Advantages

- 📆 **Year-Independent Recurring Windows**: Define periods once (e.g., October 15th to April 15th) and let them recur every year without manual yearly adjustments or fragile YAML templates.
- 🔄 **Seamless New Year Rollover**: Fully supports periods spanning across the new year (e.g., Oct 15 – Apr 15) as well as within the same calendar year (e.g., May 1 – Sep 30).
- 🎛️ **Native Helper Integration (`integration_type: helper`)**: Appears directly under Home Assistant **Settings > Devices & Services > Helpers > Create Helper**.
- ⚙️ **Config Flow & Options Flow**: Configure and tweak dates and custom icons (via MDI icon picker) entirely in the user interface.
- 🕛 **Midnight Auto-Evaluation**: Updates exactly at `00:00:00` local time via `async_track_time_change`.
- 🧮 **Rich Attributes & Countdowns**:
  - `start_date`: Formatted start (e.g., `15.10.`)
  - `end_date`: Formatted end (e.g., `15.04.`)
  - `spans_new_year`: `true` / `false`
  - `days_remaining`: Days until active period ends
  - `days_until_start`: Days until next period starts
  - `next_start`: ISO timestamp of next start date
  - `next_end`: ISO timestamp of next end date
- 🌐 **Multilingual Support**: Fully localized in English, German (`de`), and Indonesian (`id`).

---

## 📦 Installation via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=adromir&repository=ha-annual-date-period&category=integration)

1. In Home Assistant, open **HACS** > **Integrations**.
2. Click the top-right three dots menu and select **Custom repositories**.
3. Add repository URL:
   ```
   https://github.com/adromir/ha-annual-date-period
   ```
4. Category: **Integration**.
5. Click **Add**, find **Annual Date Period**, and download it.
6. Restart Home Assistant.

---

## 🚀 Creating a Helper in Home Assistant

1. Go to **Settings > Devices & Services > Helpers**.
2. Click **+ Create Helper**.
3. Choose **Annual Date Period** (or search for *Date Period* / *Heizperiode*).
4. Fill in:
   - **Name**: e.g., `Heizperiode`
   - **Start Month / Day**: e.g., `10` / `15`
   - **End Month / Day**: e.g., `04` / `15`
   - **Icon**: e.g., `mdi:radiator`
5. Click **Submit**. Your new `binary_sensor.heizperiode` is immediately ready!

---

## 💡 Example Automation Usage

### Turn on Heating Only During Heating Season

```yaml
automation:
  - alias: "Thermostate aktivieren bei Beginn der Heizperiode"
    trigger:
      - platform: state
        entity_id: binary_sensor.heizperiode
        to: "on"
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.better_thermostat_wohnzimmer
        data:
          hvac_mode: heat

  - alias: "Sommermodus: Heizung ausschalten"
    trigger:
      - platform: state
        entity_id: binary_sensor.heizperiode
        to: "off"
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.better_thermostat_wohnzimmer
        data:
          hvac_mode: "off"
```

---

## 📄 License & Disclaimer

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

This project is an independent community helper for Home Assistant and is not affiliated with or endorsed by Nabu Casa.

---

## 👤 Author

Developed by **Adromir**  
Website: [https://github.com/adromir](https://github.com/adromir)
