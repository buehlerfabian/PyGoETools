import pygoetools.goe_tools as goe
import pytest
import time


def test_get_status():
    status_raw = goe._get_status()
    assert isinstance(status_raw, dict)
    assert "car" in status_raw
    assert "psm" in status_raw
    assert "amp" in status_raw

    status = goe.get_status()
    assert isinstance(status, dict)
    assert "charging_state" in status
    assert "phase_mode" in status
    assert "current_limit" in status
    assert "charging_allowed" in status
    assert status["charging_state"] in goe.CHARGE_STATES.values()
    assert status["phase_mode"] in goe.PHASE_MODES.values()
    assert isinstance(status["current_limit"], int)
    assert status["current_limit"] >= 6
    assert status["current_limit"] <= 16
    assert status["charging_allowed"] in [True, False]

    if status_raw['frc'] == 0 or status_raw['frc'] == 2:
        assert status['charging_allowed'] is True


def test_get_charging_state():
    assert goe.get_charging_state() in goe.CHARGE_STATES.values()


def test_get_phase_mode():
    assert goe.get_phase_mode() in goe.PHASE_MODES.values()


def test_get_current_limit():
    current_limit = goe.get_current_limit()
    assert isinstance(current_limit, int)
    assert current_limit >= 6
    assert current_limit <= 16


def test_get_current_power():
    current_power = goe.get_current_power()
    assert isinstance(current_power, float)
    assert current_power >= 0


def test_get_charged_energy():
    charged_energy = goe.get_charged_energy()
    assert isinstance(charged_energy, float)
    assert charged_energy >= 0


def test_get_temperature_board():
    temperature_board = goe.get_temperature_board()
    assert isinstance(temperature_board, float)
    assert temperature_board >= -10
    assert temperature_board <= 100


def test_get_temperature_port():
    temperature_port = goe.get_temperature_port()
    assert isinstance(temperature_port, float)
    assert temperature_port >= -10
    assert temperature_port <= 100


def test_charging_allowed():
    assert goe.charging_allowed() in [True, False]


def test_set_current():
    goe.set_current(6)
    assert goe.get_current_limit() == 6

    goe.set_current(10)
    assert goe.get_current_limit() == 10

    goe.set_current(16)
    assert goe.get_current_limit() == 16

    with pytest.raises(ValueError):
        goe.set_current(5)

    with pytest.raises(ValueError):
        goe.set_current(17)

    with pytest.raises(TypeError):
        goe.set_current(6.5)

    with pytest.raises(TypeError):
        goe.set_current('6')


def test_set_phase():
    goe.set_phase(1)
    time.sleep(5)
    assert goe.get_phase_mode() == goe.PHASE_MODES[1]

    goe.set_phase(3)
    time.sleep(5)
    assert goe.get_phase_mode() == goe.PHASE_MODES[2]

    with pytest.raises(ValueError):
        goe.set_phase(2)

    with pytest.raises(ValueError):
        goe.set_phase(4)

    with pytest.raises(TypeError):
        goe.set_phase(1.5)

    with pytest.raises(TypeError):
        goe.set_phase('1')


def test_allow_charging():
    goe.allow_charging(True)
    time.sleep(5)
    assert goe.charging_allowed() is True

    time.sleep(10)
    goe.allow_charging(False)
    time.sleep(5)
    assert goe.charging_allowed() is False

    with pytest.raises(TypeError):
        goe.allow_charging(1)

    with pytest.raises(TypeError):
        goe.allow_charging('True')
