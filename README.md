# Dynamic worldclock for Home Assistant

A modified version of [worldclock](https://www.home-assistant.io/integrations/worldclock/) to support providing the time zone as a templated value.

### Installation

Take the `dynamic-worldclock` folder from this repository and copy it into your Home Assistant installation's `custom-components` folder.

### Usage

Add to your `configuration.yaml`:

```
sensor:
  - platform: "dynamic-worldclock"
    name: "Dynamic World Clock example"
    time_zone: "{{ state_attr('sensor.phone_current_time_zone', 'time_zone_id') }}"
```

### Contributions

... are very welcome, especially to fix that updates are not currently realtime (but they are fairly quick). I have very little idea of what I'm doing here.
