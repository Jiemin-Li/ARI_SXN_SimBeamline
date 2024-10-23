"""
This file will contain some generic caproto PVGroups used to generate the
beamline Caproto IOC servers
"""
from baffle_slit import BaffleSlit
from caproto.ioc_examples.fake_motor_record import FakeMotor
from caproto.server import PVGroup, SubGroup, pvproperty, ioc_arg_parser, run
from diagnostic import Diagnostic
from nslsii.iocs.eps_two_state_ioc_sim import EPSTwoStateIOC
from textwrap import dedent


class AriM3(PVGroup):
    """
    A PVGroup that generates the PVs associated with the ARI M3 mirror system.

    This class should be used to define the M3 mirror system PVs for the ARI
    beamline. It will consist of PVs for each of the motors for each mirror axis
     as well as the related vacuum component PVs.

    TODO:
    1. Decide how we want to implement the motor-record PVs.
        - Currently I use the FakeMotor PVGroup from the caproto source code,
        this does not have all of the required PVs for a motor record and so
        will need to be replaced.
        - Options I think are: 1, to use the C++ based Epics motor record
        simulated IOC or 2, to write our own Epics motor record IOC in caproto
        with only the minimum required Epics PVs for our applications (see motor
         record ophyd device for required PVs).

    Parameters
    ----------
    *args : list
        The arguments passed to the PVGroup parent class.
    **kwargs : list, optional
        The Keyword arguments passed to the PVGroup parent class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # call the PVGroup __init__ function

    # Add the mirror motor PVs.
    # Note: the angle unit is mrad and the translation unit is mm!!!
    Ry_coarse = SubGroup(FakeMotor, velocity=1, precision=3,
                         user_limits=(-10, 10), prefix=':Ry_coarse')
    Ry_fine = SubGroup(FakeMotor, velocity=0.01, precision=3,
                       user_limits=(-0.15, 0.15), prefix=':Ry_fine')
    Rz = SubGroup(FakeMotor, velocity=1, precision=3, user_limits=(-20, 20),
                  prefix=':Rz')
    x = SubGroup(FakeMotor, velocity=1, precision=3, user_limits=(-15, 5),
                 prefix=':x')

    # Add the mirror chamber vacuum PVs.
    ccg = pvproperty(value=3E-10, name=':ccg', read_only=True)
    tcg = pvproperty(value=1E-4, name=':tcg', read_only=True)
    ip = pvproperty(value=4E-10, name=':ip', read_only=True)
    gv = SubGroup(EPSTwoStateIOC, prefix=':gv:')

    # Add the baffle slit PVs.
    baffle = SubGroup(BaffleSlit, prefix=':baffle')

    # Add the diagnostic PVs.
    diag = SubGroup(Diagnostic, prefix=':diag')


# Add some code to start a version of the server if this file is 'run'.
if __name__ == "__main__":
    ioc_options, run_options = ioc_arg_parser(
        default_prefix="ARI_M1",
        desc=dedent(AriM3.__doc__))
    ioc = AriM3(**ioc_options)
    run(ioc.pvdb, **run_options)
