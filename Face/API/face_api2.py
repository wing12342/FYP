import requests

def facerec(path):
    url = "https://api.luxand.cloud/photo/search"

    payload = {}
    headers = { 'token': "5578c58e0e974c3da8473570ec5fc20a" }

    files = { "photo": open(path, "rb") }

    response = requests.request("POST", url, data=payload, headers=headers, files=files)

    data = response.json()
    if data != []:
        print(data[0]["name"])
        return True
    else:
        print("Not Found")
        return False
# print(facerec("C:\\Users\\STEM-TY\\Desktop\\fyp2\\Client_Server\\Face\\API\\Entrance\\1 2.jpg"))

def addcustomer(name, photo):
    from luxand import luxand

    client = luxand("5578c58e0e974c3da8473570ec5fc20a")

    # call SERVER function to get memberID + 1

    # client.add_person(name = "Jay", photos = ['/Users/kachunli/Desktop/FYP/facerec/images/Jay.jpg'])
    client.add_person(name = name, photos = [photo])
    print("New Customer Added")

def verify_age(path):
    url = "https://api.luxand.cloud/photo/detect"

    payload = {}
    headers = { 'token': "5578c58e0e974c3da8473570ec5fc20a" }

    files = { "photo": open(path, "rb") }

    response = requests.request("POST", url, data=payload, headers=headers, files=files)

    age_data = response.json()
    print(round(age_data[0]["age"]))

# addcustomer("Jay_C0001", "/Users/kachunli/Desktop/FYP/API/Entrance/screen'shot_2023-01-16 15:26:32.346357.png")
# verify_age("/Users/kachunli/Desktop/FYP/API/Entrance/screenshot_2023-01-16 14:18:27.131804.png")