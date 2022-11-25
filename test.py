import requests

BASE = "https://flask-production-142c.up.railway.app/"

data = [{"name":"Joe","views":100000,"likes":78},
{"name":"How to make REST API","views":80000,"likes":10000},
{"name":"Tim","views":2000,"likes":35}]

for i in range(len(data)):
    response = requests.post(BASE+"video/"+str(i+1), data = data[i])
    print(response.json())

print("GETTING STUFF")
response= requests.get(BASE+"video/1")
print(response.json())


