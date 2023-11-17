import socket
import json
import time

# Cut-the-corners TCP Client:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(('localhost', 6000))

def send_req_json(previous_bitrate,previous_list,prev_throughput,av_bitrates,chunk_arg):

    #pack message
    req = json.dumps({"Previous List" : previous_list,
                     "Previous Bitrate": previous_bitrate,
                     "Previous Throughput": prev_throughput,
                     "Available Bitrates" :av_bitrates,
                     "Chunk" : chunk_arg,
                     "exit" : 0})
    req += '\n'

    s.sendall(req.encode())

    message = ""
    while(1):
        messagepart = s.recv(2048).decode()

        #print(messagepart)
        message += messagepart
        if message[-1] == '\n':
            #print(message)

            response = json.loads(message)

            return response["delay"],response["bitrate"]


def send_exit():
    req = json.dumps({"exit" : 1})

    req += '\n'
    s.sendall(req.encode())


if __name__ == "__main__":
    pass
