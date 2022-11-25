import requests

BASE = "http://127.0.0.1:5000/"

# data = [{"name":"Joe","views":100000,"likes":78},
# {"name":"How to make REST API","views":80000,"likes":10000},
# {"name":"Tim","views":2000,"likes":35}]

# for i in range(len(data)):
#     response = requests.post(BASE+"video/"+str(i+1), data = data[i])
#     print(response.json())

# input()
response= requests.put(BASE+"video/1", data={"name":"Joe","views":1,"likes":1})
print(response.json())


