"""
This file will contain some generic caproto PVGroups used to generate the beamline
Caproto IOC servers
"""
from caproto.ioc_examples.fake_motor_record import FakeMotor
from caproto.server import PVGroup, SubGroup, ioc_arg_parser, run
from textwrap import dedent


class AriM1Mirror(PVGroup):
    """
    A PVGroup that generates the PVs associated with the ARI M1 mirror system.

    This class should be used to define the M1 mirror system PVs for the ARI beamline.
    It will consist of PVs for each of the motors for each mirror axis as well as the
    related vacuum component PVs.

    TODO:
    1. Decide if we want to have this include the baffleslit and diagnostic
       components as well:
        - This may help create a cohesive connection between them but also blurs
          the lines between vacuum sections and physical devices.
    2. Add the vacuum component (gauges, pumps, valves, ....).
        - This may require defining vacuum component PVGroups.

    Parameters
    ----------
    *args : list
        The arguments passed to the PVGroup parent class
    **kwargs : list, optional
        The Keyword arguments passed to the PVGroup parent class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # call the PVGroup __init__ function

    Ry_coarse = SubGroup(FakeMotor, velocity=0.1, precision=6E-5, acceleration=1.0,
                         resolution=6E-5, user_limits=(-3.15, -1.15), tick_rate_hz=10.,
                         prefix='Ry_coarse')
    Ry_fine = SubGroup(FakeMotor, velocity=0.1, precision=6E-7, acceleration=1.0,
                       resolution=6E-7, user_limits=(-0.03, 0.03), tick_rate_hz=10.,
                       prefix='Ry_fine')
    Rz = SubGroup(FakeMotor, velocity=0.1, precision=6E-5, acceleration=1.0,
                  resolution=6E-5, user_limits=(-2.3, 2.3), tick_rate_hz=10.,
                  prefix='Rz')
    x = SubGroup(FakeMotor, velocity=0.0001, precision=5., acceleration=1.0,
                 resolution=5., user_limits=(-10000., 10000.), tick_rate_hz=1E-3,
                 prefix='x')
    y = SubGroup(FakeMotor, velocity=0.1, precision=5., acceleration=1.0,
                 resolution=5., user_limits=(-10000., 10000.), tick_rate_hz=10.,
                 prefix='y')


# Add some code to start a version of the server if this file is 'run'.
if __name__ == "__main__":
    ioc_options, run_options = ioc_arg_parser(
        default_prefix="ARI:M1:",
        desc=dedent(AriM1Mirror.__doc__))
    ioc = AriM1Mirror(**ioc_options)
    run(ioc.pvdb, **run_options)