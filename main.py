import requests
import pyrfc6266

url = 'http://httpbin.org/response-headers?Content-Disposition=attachment;%20filename%3d%22foo.html%22'
url = 'https://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf'
url = 'https://www.businessregistry.gr/downloadFile/index?key=assemblyDecision&elementId=3113977'
response = requests.get(url)
file_name = pyrfc6266.requests_response_to_filename(response)
print(file_name)
