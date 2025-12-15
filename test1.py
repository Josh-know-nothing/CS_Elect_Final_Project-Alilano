import requests
import jwt



BASE_URL = "http://127.0.0.1:5000/api"
SECRET_KEY = "CSelect1"

# Generate JWT token for protected routes
token = jwt.encode({"user": "test"}, SECRET_KEY, algorithm="HS256")
HEADERS = {"Authorization": token}


# GET ALL STUDENTS

print("GET ALL STUDENTS ")
resp = requests.get(f"{BASE_URL}/students")
print("Status code:", resp.status_code)
try:
    print(resp.json())
except:
    print(resp.text)


# ADD A NEW STUDENT

print("\n ADD STUDENT ")
new_student = {
    "first_name": "Tester",
    "last_name": "teester",
    "age": 50,
    "gender": "Male",
    "course_id": 21
}
resp = requests.post(f"{BASE_URL}/student", json=new_student, headers=HEADERS)
print("Status code:", resp.status_code)
try:
    print(resp.json())
except:
    print(resp.text)


# SERCH STUDENT

print("\nSEARCH STUDENT ")
search_name = "Joshua"
resp = requests.get(f"{BASE_URL}/student/search?name={search_name}")
print("Status code:", resp.status_code)
try:
    print(resp.json())
except:
    print(resp.text)


# UPDATE STUDENT

print("\n UPDATE STUDENT ")

student_id_to_update = 20
update_data = {
    "first_name": "Ruy",
    "last_name": "Lopez Gambit",
    "age": 30,
    "gender": "Male",
    "course_id": 3
}
resp = requests.put(f"{BASE_URL}/student/{student_id_to_update}", json=update_data, headers=HEADERS)
print("Status code:", resp.status_code)
try:
    print(resp.json())
except:
    print(resp.text)


# DELETE STUDENT

print("\nDELETE STUDENT")

student_id_to_delete = 19
resp = requests.delete(f"{BASE_URL}/student/{student_id_to_delete}", headers=HEADERS)
print("Status code:", resp.status_code)
try:
    print(resp.json())
except:
    print(resp.text)
