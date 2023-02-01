
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

def addItem(item):
    if item not in itemList:
        itemList.append(item)
    print('itemList:')
    print(itemList)
    
itemList = []
ser = serial.Serial('COM6', 57600)
ser.isOpen()
print("start")

receivedBytes = bytearray()

try:
    count=0
    while True:
        pass
        print(f'First:+{itemList}')
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
            #compare(itemList,sqlitemList)
            data = {'cart': itemList}
            res = requests.post('http://127.0.0.1:3000/shoppingcart', json=data)
            returned_data = res
            # print(returned_data)
            # door(returned_data['result'])

            itemList.clear()
            count=0
            time.sleep(3)
        count+=1        
except KeyboardInterrupt:
    pass




#if check user id by face checking for purchasing
# if else reset by set limited time
ser.close()


