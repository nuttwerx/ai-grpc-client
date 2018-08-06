import client as ct
import brain as bn

# Initializes client and Q-learning model.
client = ct.GrpcClient()
brain = bn.Dqn(8,8,0.99)
client.add_listener(brain)

# Starts client listening and gets streamed values.
while client.listen():
    print("Listening...")

# Updates Q-learning model with streamed values, and gets optimized output.
# TODO: implement proper reward function as input to `reward`.
# TODO: understand the format of `output` (`action` in brain).

# Sends optimized output back to client.
#client.send_command(output)