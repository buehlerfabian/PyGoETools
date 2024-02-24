import pygoetools.goe_tools as goe
import pytest
import time


def test_get_status():
    status = goe.get_status()
    assert isinstance(status, dict)
    assert "car" in status
    assert "psm" in status
    assert "amp" in status


def test_get_charging_state():
    assert goe.get_charging_state() in goe.CHARGE_STATES.values()


def test_get_phase_mode():
    assert goe.get_phase_mode() in goe.PHASE_MODES.values()


def test_get_current_limit():
    current_limit = goe.get_current_limit()
    assert isinstance(current_limit, int)
    assert current_limit >= 6
    assert current_limit <= 16


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
