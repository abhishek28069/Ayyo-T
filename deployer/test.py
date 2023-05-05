import socket

def find_free_port():
    # create a temporary socket to find a free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # bind to any available port
        port = s.getsockname()[1]  # get the assigned port
    return port

print(type(find_free_port()))