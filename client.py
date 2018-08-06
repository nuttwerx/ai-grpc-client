import grpc
import brain
import groundstation_pb2
import groundstation_pb2_grpc

FCU = "Flight Control"

STREAM_ACCEL_ON = [FCU, 0x0100100, [0x00000001, 0x00001003, 0x0, 0x0]]
STREAM_ACCEL_OFF = [FCU, 0x0100100, [0x00000000, 0x00001003, 0x0, 0x0]]
STREAM_LASER_FWD_ON = [FCU, 0x0100100, [0x00000001, 0x00001201, 0x0, 0x0]]
STREAM_LASER_FWD_OFF = [FCU, 0x0100100, [0x00000000, 0x00001201, 0x0, 0x0]]

ACTIONS = [STREAM_ACCEL_ON,
           STREAM_ACCEL_OFF,
           STREAM_LASER_FWD_ON,
           STREAM_LASER_FWD_OFF]

PARAM_LIST = ["Accel 1 Current Accel",
              "Accel 2 Current Accel",
              "Accel 1 X Raw","Accel 1 Y Raw","Accel 1 Z Raw",
              "Accel 2 X Raw","Accel 2 Y Raw","Accel 2 Z Raw",
              ]


class GrpcClient():
    def __init__(self):
        # establishing the connection to the groundstation
        self.channel = grpc.insecure_channel('localhost:9800')
        # setting up the allowed methods on the connection
        self.stub = groundstation_pb2_grpc.GroundStationServiceStub(self.channel)
        self.listeners = []

    def add_listener(self,listener):
        self.listeners.append(listener)

    def send_command(self,command):
        cmd = groundstation_pb2.Command(Node=command[0],PacketType=command[1],Data=command[2])
        self.stub.sendCommand(cmd)

    def listen(self):
        # request object that specifies which parameters we would like to receive
        request = groundstation_pb2.StreamRequest(All=False, Parameters=PARAM_LIST)
        # this action sends the request to the ground station and returns a stream
        data_stream = self.stub.streamPackets(request)
        for dataBundle in data_stream:
            # retrieve the data array
            parameters = dataBundle.Parameters
            values = []
            parameters.sort(key=lambda param: param.ParamName)
            for param in parameters:
                val = extract_value(param)
                values.append(val)
            for listener in self.listeners:
                output = listener.update(100,values)


def extract_value(parameter):
    if parameter.Value.Index == 1:
           return parameter.Value.Int64Value
    elif parameter.Value.Index == 2:
        return parameter.Value.Uint64Value
    elif parameter.Value.Index == 3:
        return parameter.Value.DoubleValue


if __name__ == '__main__':
    client = GrpcClient()
    client.listen()