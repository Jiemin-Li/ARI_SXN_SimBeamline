from caproto.ioc_examples.fake_motor_record import FakeMotor
from caproto.server import PVGroup, SubGroup, ioc_arg_parser, run
from four_blade_electrometer import FourBladeElectrometer
from textwrap import dedent


class BaffleSlit(PVGroup):
    """
    A PVGroup that generates the PVs associated with the ARI M1 mirror system.

    This class should be used to define the Baffle Slit system PVs for the baffle slits
    used in the ARI and SXN beamlines. It will consist of PVs for each of the associated
    motors for each baffle as well as the photo-current PVs from each of the blades.

    TODO:
    1. Work out how we want to define the area detector PVs, including how we 'update'
       the photo-current PVs based from each of the blades when the mirror and/or baffles
       are moved.
    2. Decide how we want to implement the motor-record PVs.
        - See the section in the AriM1Mirror PVGroup below on this topic.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # call the PVGroup __init__ function

    # Add the baffle motor PVs.
    top = SubGroup(FakeMotor, velocity=0.1, precision=6E-3, acceleration=1.0,
                   resolution=6E-3, user_limits=(-1, 20), tick_rate_hz=10.,
                   prefix=':top')
    bottom = SubGroup(FakeMotor, velocity=0.1, precision=6E-3, acceleration=1.0,
                      resolution=6E-3, user_limits=(-20, 1), tick_rate_hz=10.,
                      prefix=':bottom')
    inboard = SubGroup(FakeMotor, velocity=0.1, precision=6E-3, acceleration=1.0,
                       resolution=6E-3, user_limits=(-20, 1), tick_rate_hz=10.,
                       prefix=':inboard')
    outboard = SubGroup(FakeMotor, velocity=0.1, precision=6E-3, acceleration=1.0,
                        resolution=6E-3, user_limits=(-1, 20), tick_rate_hz=10.,
                        prefix=':outboard')

    current = SubGroup(FourBladeElectrometer, prefix=':current')


# Add some code to start a version of the server if this file is 'run'.
if __name__ == "__main__":
    ioc_options, run_options = ioc_arg_parser(
        default_prefix="BaffleSlit",
        desc=dedent(BaffleSlit.__doc__))
    ioc = BaffleSlit(**ioc_options)
    run(ioc.pvdb, **run_options)