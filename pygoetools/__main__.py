import sys
import argparse
import pygoetools.goe_tools as goe


def main():
    # set up parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, choices=range(6, 17),
                        help='set charging current')
    parser.add_argument('-p', help='set phase mode', type=int,
                        choices=[1, 3])
    startstop_group = parser.add_mutually_exclusive_group()
    startstop_group.add_argument('--stop', help='stops charging',
                                 action='store_true')
    startstop_group.add_argument('--start', help='start charging',
                                 action='store_true')
    args = parser.parse_args()

    # process arguments
    if args.stop:
        goe.allow_charging(False)

    if args.c is not None:
        goe.set_current(args.c)

    if args.p is not None:
        goe.set_phase(args.p)

    if args.start:
        goe.allow_charging(True)

    # print current status
    status = goe.get_status()
    print(f'Charging state: {status["charging_state"]}')
    print(f'Charging allowed: {status["charging_allowed"]}')
    print(f'Phase mode: {status["phase_mode"]}')
    print(f'Current limit: {status["current_limit"]}A')


if __name__ == "__main__":
    sys.exit(main())
