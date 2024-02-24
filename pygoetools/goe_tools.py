import requests
import json
import config


CHARGE_STATES = {1: 'not connected', 2: 'charging',
                 3: 'waiting for car', 4: 'charging finished'}
PHASE_MODES = {1: '1-Phase', 2: '3-Phase'}
FORCE_STATE_MODES = {0: 'Neutral', 1: 'Off', 2: 'On'}


class OperationFailedError(Exception):
    pass


def get_status():
    dat = requests.get(f'{config.goe_url}/api/status').text
    status_dict = json.loads(dat)
    return status_dict


def get_charging_state():
    status_dict = get_status()
    return CHARGE_STATES[status_dict["car"]]


def get_phase_mode():
    status_dict = get_status()
    return PHASE_MODES[status_dict["psm"]]


def get_current_limit():
    status_dict = get_status()
    return int(status_dict["amp"])


def charging_allowed():
    status_dict = get_status()
    return status_dict["frc"] == 0 or status_dict["frc"] == 2


def set_current(current):
    if not isinstance(current, int):
        raise TypeError('current must be an integer between 6A and 16 A')
    if current < 6 or current > 16:
        raise ValueError('current must be between 6A and 16 A')
    req = requests.get(f'{config.goe_url}/api/set?amp={current}')
    if req.status_code != 200:
        raise OperationFailedError(f'Error setting current to {current} A')


def set_phase(phase):
    if not isinstance(phase, int):
        raise TypeError('Phase setting must be an integer (1 or 3).')
    if phase not in [1, 3]:
        raise ValueError('Phase setting must be 1 or 3.')

    if phase == 1:
        req = requests.get(f'{config.goe_url}/api/set?psm=1')
        if req.status_code != 200:
            raise OperationFailedError(
                'Changing to 1 phase charging mode not successful.')
    else:
        req = requests.get(f'{config.goe_url}/api/set?psm=2')
        if req.status_code != 200:
            raise OperationFailedError(
                'Changing to 3 phase charging mode not successful.')


def set_charging_allowed(allowed):
    if not isinstance(allowed, bool):
        raise TypeError('allowed must be a boolean.')
    if allowed:
        req = requests.get(f'{config.goe_url}/api/set?frc=0')
    else:
        req = requests.get(f'{config.goe_url}/api/set?frc=1')
    if req.status_code != 200:
        raise OperationFailedError(
            f'Error setting charging allowed to {allowed}')
