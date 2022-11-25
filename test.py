import requests

BASE = "http://127.0.0.1:5000/"

# data = [{"name":"Joe","views":100000,"likes":78},
# {"name":"How to make REST API","views":80000,"likes":10000},
# {"name":"Tim","views":2000,"likes":35}]

# for i in range(len(data)):
#     response = requests.post(BASE+"video/"+str(i+1), data = data[i])
#     print(response.json())

# print("GETTING STUFF")
response= requests.get(BASE+"video/1", headers= {'token':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiQnJ5YW4iLCJleHBpcmF0aW9uIjoiMjAyMi0xMS0yNSAxMzozNjoyNi45MTY3NDAifQ.dQZWpwCi6F7q-sVVRIoJqsq9wKgbVgwAQ7DBXVtupTE'})
print(response.json())
# response = requests.post(BASE+"login", data = {'username':'Bryan','password':123456})
# print(response.json())

