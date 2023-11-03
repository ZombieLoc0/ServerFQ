from threading import Thread, activeCount
import socket

#region SOCKET VARIABLES
HEADER = 64
PORT = 5050 
SERVER = socket.gethostbyname(socket.gethostname())   #Obtener direccion IP de la computadora
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
#endregion

#Shared Variables
item_queues = []

def put_in_queue(item):
    for q in item_queues:
        if item == q[0]:
            q.append(item)
            return
        
    item_queues.append([item,item])

def send_item(request):
    index = int(request[0])
    item = 'xy'
    print(item_queues, len(item_queues))

    if index >= len(item_queues):
            index = 0
            item = item.replace('y','t')
    try:
        item = item.replace('x', item_queues[index].pop(1))
    except:
       item = item.replace('x', 'n')

    return item
    
def client_handler(conn, addr):
    connected = True
    while connected:
        #arreglar: Se recive un dato vacio
        msg_lenght = conn.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)

            if msg_lenght == 1:             #Los mensajes de la terminal son tamano 1
                msg = conn.recv(msg_lenght).decode(FORMAT)
                print(f'[Se recive: {addr}]El item: -{msg}')
                put_in_queue(msg)
            elif msg_lenght > 1:            #Es un request del cashier es tamano 2 (o mas)
                msg = conn.recv(msg_lenght).decode(FORMAT)
                print(f'Mensaje recivido: {msg}')
                if msg == '90':
                    break
                item  = send_item(msg)

                conn.send(item.encode(FORMAT))
                print(f'[Se envia a: {addr}]-El item: {item}')
            
    conn.close()

def start_server():
    server.listen()

    while True:
        conn, addr = server.accept()
        client_thread = Thread(target=client_handler, args=(conn, addr))
        client_thread.start()

        print('[NUEVA CONEXION]')
        print(f'[CONEXIONES ACTIVAS] - {activeCount()-1}')


start_server()