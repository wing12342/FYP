
import serial
import requests
import time
NUMBER_OF_BYTE = 18

def CRC_check(b_array):
    CRC = 0xFFFF
    index = 0
    for b in b_array:
        CRC ^= b
        for i in range(8, 0,-1):
            if ((CRC & 0x0001) != 0):
                CRC >>= 1
                CRC ^= 0x8408
            else:
                CRC >>= 1
        index += 1
        if index >= (NUMBER_OF_BYTE - 2):
            break
    if (b_array[NUMBER_OF_BYTE - 2] == (CRC & 0x00FF)) and (b_array[NUMBER_OF_BYTE - 2] == ((CRC & 0xFF00 >> 8))):
        return True
    else:
        return False

def connectServerGetItem(sqlitemList):
    array = [1,2,3,4,5,6,7,8,9,10]
    data = {'array':array}

    # The POST request to our node server
    res = requests.post('http://127.0.0.1:3000/getItem', json=data)

    # Convert response data to json
    returned_data = res.json()
    for x in range(0,len(returned_data)):
        sqlitemList.append(returned_data[x]['rfid'])

def compare(itemList,sqlitemList):
    set1 = set(itemList)
    set2 = set(sqlitemList)

    missing = list(sorted(set1-set2))
    print('missing:')
    print(missing)




def addItem(item):
    if item not in itemList:
        itemList.append(item)
    print('item added in itemList:')
    print(item)
    

ser = serial.Serial('COM6', 57600)
ser.isOpen()
print("start")

receivedBytes = bytearray()

itemList = []
sqlitemList = []
try:
    count=0
    connectServerGetItem(sqlitemList)
    while True:
        pass
        print('sqlitemList From SQL:')
        print(sqlitemList)
        print(f'itemList:+{itemList}')
        if ser.in_waiting:
            tmp = ser.read()
            receivedBytes += tmp
            
            if len(receivedBytes) == 18:
                print(receivedBytes.hex())
                epc = str(receivedBytes.hex())
                epc = epc[8:32]
                #print("epc: " + epc)
                #print(CRC_check(receivedBytes))
                receivedBytes = bytearray()
                addItem(epc)
        if count>1000:
            compare(itemList,sqlitemList)
            itemList.clear()
            count=0
            time.sleep(3)
        count+=1        
except KeyboardInterrupt:
    pass




#if check user id by face checking for purchasing
# if else reset by set limited time
ser.close()


