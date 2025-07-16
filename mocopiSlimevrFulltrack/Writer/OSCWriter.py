from pprint import pprint

from pythonosc.udp_client import UDPClient as OSCClient
from pythonosc.osc_bundle_builder import OscBundleBuilder
from pythonosc.osc_message_builder import build_msg

from pxr import Gf


from .BaseWriter import BaseWriter
from .skelTree import MOCOPI_SKEL_NAMES


class OSCWriter(BaseWriter):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        kwargs["stride"] = 1
        super().__init__(*args, **kwargs)
        self.__target_addr = "127.0.0.1"
        self.__target_port = 9001

        self.__osc_client = OSCClient(self.__target_addr, self.__target_port)

    def close(self):
        pass

    def _writeAnimation(self, base, samples):
        builder = OscBundleBuilder(0)

        skel = samples[base]["btrs"]
        head = skel[10]["tran"]

        builder.add_content(
            build_msg("/tracking/trackers/head/position", head["translation"])
        )
        rot = Gf.Rotation(
            Gf.Quatd(
                head["rotation"][3],
                head["rotation"][0],
                head["rotation"][1],
                head["rotation"][2],
            )
        ).Decompose(
            Gf.Vec3d(0, 0, 1),
            Gf.Vec3d(1, 0, 0),
            Gf.Vec3d(0, 1, 0),
        )
        builder.add_content(build_msg("/tracking/trackers/head/rotation", list(rot)))
        self.__osc_client.send(builder.build())

    def flushTimesample(self):
        pass


__all__ = ["OSCWriter"]
