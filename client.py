import grpc
import groundstation_pb2
import groundstation_pb2_grpc

FCU = "Flight Control"

STREAM_ACCEL_ON = [FCU, 0x0100, [0x00000001, 0x00001003, 0x0, 0x0]]
STREAM_ACCEL_OFF = [FCU, 0x0100, [0x00000000, 0x00001003, 0x0, 0x0]]
STREAM_LASER_FWD_ON = [FCU, 0x0100, [0x00000001, 0x00001201, 0x0, 0x0]]
STREAM_LASER_FWD_OFF = [FCU, 0x0100, [0x00000000, 0x00001201, 0x0, 0x0]]

ACTIONS = [STREAM_ACCEL_ON,STREAM_ACCEL_OFF,STREAM_LASER_FWD_ON,STREAM_LASER_FWD_OFF]


class GrpcClient():
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:9800')
        self.stub = groundstation_pb2_grpc.GroundStationServiceStub(self.channel)
        self.listeners = []

    def add_listener(self,listener):
        self.listeners.append(listener)

    def send_command(self,command):
        cmd = groundstation_pb2.Command(Node=command[0],PacketType=command[1],Data=command[2])
        self.stub.sendCommand(command)

    def listen(self):
        request = groundstation_pb2.StreamRequest()
        data_stream = self.stub.streamPackets(request)

        for dataBundle in data_stream:
            parameters = dataBundle.Parameters
            values = []
            parameters.sort(key=lambda param: param.ParamName)
            for param in parameters:
                # do whatever action you want here
                val = extract_value(param)
                values.append(val)
            for listener in self.listeners:
                listener.newData(values)


def extract_value(parameter):
    if parameter.Value.Index == 1:
           return parameter.Value.Int64Value
    elif parameter.Value.Index == 2:
        return parameter.Value.Uint64Value
    elif parameter.Value.Index == 3:
        return parameter.Value.Index.DoubleValue


if __name__ == '__main__':
    client = GrpcClient()
    client.listen()