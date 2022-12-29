import serial.tools.list_ports
import time
import sys
from Adafruit_IO import MQTTClient

AIO_FEED_IDS = ["bbc-soil", "bbc-relay"]
AIO_USERNAME = "piquihac"
AIO_KEY = "aio_RxUX00PN2e0uZeZFCLE2lodFmVHf"

def connected(client):
    print("Ket noi thanh cong ...")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + feed_id + payload)
    if isMicrobitConnected:
        if(feed_id == "bbc-relay"):
            ser.write((str(payload)).encode())
            print(str(payload))

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB-SERIAL" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

isMicrobitConnected = False
if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    isMicrobitConnected = True

mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = ser.read(bytesToRead).decode("UTF-8")
        client.publish("bbc-soil", mess[0:len(mess)])

client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_subscribe = subscribe
client.on_message = message
client.connect()
client.loop_background()
time.sleep(2)

while True:
    if isMicrobitConnected:
        readSerial()
    time.sleep(1)
