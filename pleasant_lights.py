blueprint:
  name: Pleasant lights
  description: Turn lights on when it's dark, but off in the middle of the night unless the sometning is on ( door open, motion etc) .
  domain: automation
  input:
    light:
      name: Light
      selector:
        entity:
          domain: light
    sunlight_sensor:
      name: Sunlight sensor
      selector:
        entity:
          domain: binary_sensor
    door_sensor:
      name: Something sensor
      selector:
        entity:
          domain: binary_sensor
    night_time:
      name: Night time
      description: "What time at night should the lights turn off"
      default: "23:00"
      selector:
        time:
    morning_time:
      name: Day time
      description: "What time in the morning should the lights turn on"
      default: "05:30"
      selector:
        time:


trigger:
- platform: time
  at: !input morning_time
- platform: time
  at: !input night_time
- platform: state
  entity_id: !input door_sensor
- platform: state
  entity_id: !input sunlight_sensor
- platform: homeassistant
  event: start
- platform: state
  entity_id: !input light
  from: unavailable

condition: []

action:
- choose:
  - conditions:
    - condition: state
      state: "on"
      entity_id: !input sunlight_sensor
    sequence:
    - service: light.turn_off
      entity_id: !input light
  - conditions:
    - condition: state
      entity_id: !input door_sensor
      state: "on"
    sequence:
    - service: light.turn_on
      entity_id: !input light
  - conditions:
    - condition: time
      after: !input morning_time
      before: !input night_time
    sequence:
    - service: light.turn_on
      entity_id: !input light
  default:
  - service: light.turn_off
    entity_id: !input light
