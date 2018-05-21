import grpc
import groundstation_pb2
import groundstation_pb2_grpc

FCU = "Flight Control"

STREAM_ACCEL_ON = [FCU, 0x0100, [0x00000001, 0x00001003, 0x0, 0x0]]
STREAM_ACCEL_OFF = [FCU, 0x0100, [0x00000000, 0x00001003, 0x0, 0x0]]
STREAM_LASER_FWD_ON = [FCU, 0x0100, [0x00000001, 0x00001201, 0x0, 0x0]]
STREAM_LASER_FWD_OFF = [FCU, 0x0100, [0x00000000, 0x00001201, 0x0, 0x0]]

class GrpcClient():
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:9800')
        self.stub = groundstation_pb2_grpc.GroundStationServiceStub(self.channel)
        self.listener = []

    def add_listener(self,listener):
        self.listener.append(listener)

    def send_command(self,command):
        cmd = groundstation_pb2.Command(Node=command[0],PacketType=command[1],Data=command[2])
        self.stub.sendCommand(command)

    def listen(self):
        print("-------------- startstream --------------")
        request = groundstation_pb2.StreamRequest()
        data_stream = self.stub.streamPackets(request)

        for dataBundle in data_stream:
            for data in dataBundle.Parameters:
                # do whatever action you want here
                print('whatever')


if __name__ == '__main__':
    client = GrpcClient()
    client.listen()