import requests
#url = "http://35.186.154.17:8000/traindata"
url = "http://app.bookcommerce.com/api/webservice/SaveNonBookScrapperFile"
files = {'media': open('data.json', 'rb')}
r = requests.post(url, files=files)
#r = requests.post(url)
print(r.json())