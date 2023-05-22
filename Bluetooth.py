import uuid
import bluetooth
'''
sudo sdptool add SP
sudo hcitool dev
sudo hciconfig hci0 piscan
'''
server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))
server_socket.listen(1)
port = server_socket.getsockname()[1]
service_id = str(uuid.uuid4())
 
bluetooth.advertise_service(server_socket, "LEDServer",
                  service_id = service_id,
                  service_classes = [service_id, bluetooth.SERIAL_PORT_CLASS],
                  profiles = [bluetooth.SERIAL_PORT_PROFILE])
def bluetooth():
    try:
        print('按下 Ctrl-C 可停止程式')
        while True:
            print('等待 RFCOMM 頻道 {} 的連線'.format(port))
            client_socket, client_info = server_socket.accept()
            print('接受來自 {} 的連線'.format(client_info))
            try:
                print("1")
                while True:
                    data = client_socket.recv(1024).decode().lower()
                    if len(data) == 0:
                        break
                    if data == 'cold':
                        print('冷水')
                        Temp = 'cold'
                    elif data == 'warm':
                        print('溫水')
                        Temp = 'warm'
                    elif data == 'hot':
                        print('熱水')
                        Temp = 'hot'
                    elif data == 'two':
                        print('200ml')
                        Vol = '200ml'
                    elif data == 'four':
                        print('400ml')
                        Vol = '400ml'
                    elif data == 'six':
                        print('600ml')
                        Vol = '600ml'
                    elif data == 'confirm':
                        print('確認')
                        OP1 = Temp
                        OP2 = Vol
                        break
                    elif data == 'reselect':
                        print('重新選擇')
                    else:
                        print('未知的指令: {}'.format(data))
            except IOError:
                pass
            client_socket.close()
            print('中斷連線')
            return OP1,OP2
    except KeyboardInterrupt:
        print('中斷程式')
    finally:
        '''
        if 'client_socket' in vars():
            client_socket.close()
        server_socket.close()
        '''
        print('中斷連線')

if __name__ == "__main__":
    a,b = bluetooth()
    print(f'Temp = {a}\nVol = {b}')
