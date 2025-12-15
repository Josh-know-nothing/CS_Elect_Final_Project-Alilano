import requests

BASE_URL = "http://127.0.0.1:5000/api"


# LOGIN TO GET JWT TOKEN

login_data = {
    "username": "admin",
    "password": "admin123"
}
resp = requests.post(f"{BASE_URL}/login", json=login_data)
if resp.status_code == 200:
    token = resp.json()["token"]
    HEADERS = {"Authorization": token}
    print("Login successful. Token obtained.")
else:
    print("Login failed:", resp.status_code, resp.text)
    exit()


# GET ALL STUDENTS

print("\nGET ALL STUDENTS")
resp = requests.get(f"{BASE_URL}/students")
print("Status code:", resp.status_code)
try:
    print(resp.json())
except:
    print(resp.text)


# ADD A NEW STUDENT

print("\nADD STUDENT")
new_student = {
    "first_name": "Tester",
    "last_name": "Teester",
    "age": 50,
    "gender": "Male",
    "course_id": 9
}
resp = requests.post(f"{BASE_URL}/student", json=new_student, headers=HEADERS)
print("Status code:", resp.status_code)
try:
    print(resp.json())
except:
    print(resp.text)


# SARCH STUDENT

print("\nSEARCH STUDENT")
search_name = "Tester"
resp = requests.get(f"{BASE_URL}/student/search?name={search_name}")
print("Status code:", resp.status_code)
try:
    print(resp.json())
except:
    print(resp.text)


# UPDATE STUDENT

print("\nUPDATE STUDENT")
student_id_to_update = 17
update_data = {
    "first_name": "Updated",
    "last_name": "Student",
    "age": 51,
    "gender": "Male",
    "course_id": 2
}
resp = requests.put(f"{BASE_URL}/student/{student_id_to_update}", json=update_data, headers=HEADERS)
print("Status code:", resp.status_code)
try:
    print(resp.json())
except:
    print(resp.text)


#  DELETE STUDENT

print("\nDELETE STUDENT")
student_id_to_delete = 20
resp = requests.delete(f"{BASE_URL}/student/{student_id_to_delete}", headers=HEADERS)
print("Status code:", resp.status_code)
try:
    print(resp.json())
except:
    print(resp.text)
