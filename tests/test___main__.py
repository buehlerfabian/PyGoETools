import pygoetools.__main__ as main
import pygoetools.goe_tools as goe
import pytest
import time
import sys


def test_main_stop_charging():
    goe.allow_charging(True)
    time.sleep(5)
    assert goe.charging_allowed() is True

    sys.argv = ['pygoetools', '--stop']
    main.main()

    time.sleep(5)
    assert goe.charging_allowed() is False


def test_main_set_current():
    sys.argv = ['pygoetools', '-c 8']
    main.main()

    assert goe.get_current_limit() == 8

    sys.argv = ['pygoetools', '-c 20']
    with pytest.raises(SystemExit):
        main.main()

    assert goe.get_current_limit() == 8


def test_main_set_phase():
    sys.argv = ['pygoetools', '-p 1']
    main.main()

    time.sleep(5)
    assert goe.get_phase_mode() == goe.PHASE_MODES[1]

    sys.argv = ['pygoetools', '-p 2']
    with pytest.raises(SystemExit):
        main.main()

    assert goe.get_phase_mode() == goe.PHASE_MODES[1]

    sys.argv = ['pygoetools', '-p 3']
    main.main()

    time.sleep(5)
    assert goe.get_phase_mode() == goe.PHASE_MODES[2]


def test_main_start_charging():
    goe.allow_charging(False)
    time.sleep(5)
    assert goe.charging_allowed() is False

    sys.argv = ['pygoetools', '--start']
    main.main()

    time.sleep(5)
    assert goe.charging_allowed() is True


def test_main_print_status(capsys):
    sys.argv = ['pygoetools']
    main.main()

    captured = capsys.readouterr()
    assert "Charging state: " in captured.out
    assert "Charging allowed: " in captured.out
    assert "Phase mode: " in captured.out
    assert "Current limit: " in captured.out
