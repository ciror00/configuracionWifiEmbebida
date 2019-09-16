import os
import machine
import time
import network
import socket


def web_page():
    html = """<!DOCTYPE html>
  <html>
	<head>
		<title>Pyrague</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="icon" href="data:,">
		<style>html{font-family: Arial; display:inline-block; margin: 0px auto; text-align: center;}
		h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #088A08; border: none; 
		border-radius: 4px; color: white; padding: 0px 100px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}}
		</style><!-- file:///X:/?ssid=asd&pass=asd -->
	</head>
	<body> <h1>CONECTARSE A UNA RED</h1> 
		<form action="/" id="form">
			<p><strong>INGRESE LOS DATOS</strong></p>
			<p><a>SSID: <input type="text" name="ssid"></a></p>
			<p><a>PASSWORD: <input type="password" name="pasw"></a></p>
			<p><a><button class="button">Enviar</button></a></p>
		</form>
	</body>
  </html>
  """
    return html


class Connectivity:
    def __init__(self):
        # Configuracion de AP
        self.ap_ssid = "Pyrague"
        self.ap_password = "123456789"
        self.ap_if = network.WLAN(network.AP_IF)
        time.sleep(1)
        self.network_wifi = None
        self.password_wifi = None
        # Configuracion de STA
        self.sta_if = network.WLAN(network.STA_IF)
        time.sleep(1)

    def update(self):
        try:
            os.remove("network.txt")
            print("network.txt eliminado")
        except:
            print("No existe network.txt o no se puedo eliminar")
        file = open("network.txt", "w")
        file.write(self.network_wifi)
        file.write("\n")
        file.write(self.password_wifi)
        file.close()

    def backup(self):
        try:
            file = open("network.txt", "r")
            read = file.readlines()
            print(read)
            self.network_wifi = read[0]
            self.password_wifi = read[1]
            return True
        except:
            return False

    def wifi(self, ssid_flash=0, password_flash=0):
        if (ssid_flash == 0):
            ssid = str(self.network_wifi)
            pasw = str(self.password_wifi)
        else:
            ssid = str(ssid_flash)
            pasw = str(password_flash)
        print('Iniciando conexion Wifi en la red %s', ssid)
        # time = 60
        self.ap_if.active(False)
        time.sleep(1)
        self.sta_if.active(True)
        if (self.network_wifi != None):
            if not self.sta_if.isconnected():
                print('connecting to network...')
                self.sta_if.connect(ssid, pasw)
                while not self.sta_if.isconnected():
                    pass
            print('Network config:', self.sta_if.ifconfig())
        else:
            print('No se encontro RED configurada.')

    def server(self):
        self.sta_if.active(False)
        time.sleep(1)
        self.ap_if.active(True)
        self.ap_if.config(essid=self.ap_ssid, password=self.ap_password)
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)

        print('listening on', addr)

        while True:
            conn, addr = s.accept()
            print('Client connected from %s' % str(addr))
            time.sleep(1)
            request = conn.recv(1024)
            request = str(request)
            # print(str(request, 'utf8'), end='')
            time.sleep(1)
            ssid_position = request.find('/?ssid=')
            pasw_position = request.find('&pasw=')
            cut_position = request.find('HTTP')
            if (ssid_position != -1):
                self.network_wifi = str(request[ssid_position * 2 + 1:pasw_position])
                self.password_wifi = str(request[pasw_position + 6:cut_position - 1])
                print('\n')
                # print('SSID = %s' % self.network_wifi)
                # print('PASSWORD = %s' % self.password_wifi)
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.close()
                break
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        print('Se cargaron datos de red para conexion Wifi')
