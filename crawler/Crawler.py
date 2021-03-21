import requests
import json

code = "COMP1000"
query = 'mq2_psubject.code: \"'+code+'\"'

# url to the website's api handler
url = "https://coursehandbook.mq.edu.au/api/es/search"
# json data to parse to get the info, gotten from chrome's networking tab under the "search" item
data = {"query":{"bool":{"must":[{"query_string":{"query":query}},{"term":{"live":"true"}}]}},"aggs":{"implementationYear":{"terms":{"field":"mq2_psubject.implementationYear_dotraw","size":100}},"availableInYears":{"terms":{"field":"mq2_psubject.availableInYears_dotraw","size":100}}},"size":100,"_source":{"includes":["versionNumber","availableInYears","implementationYear"]}}
# headers so it knows we're attaching json
headers = {'content-type': 'application/json'}

# send the request
r = requests.post(url, data=json.dumps(data), headers=headers)
if r.status_code == 200:
    output = r.json()
    contentlets = output.get('contentlets')
    for a in contentlets:
        for b in a:
            print(str((b)))
        print("\n\n\n--STOP--\n\n\n")
else:
    print("Error encountered: "+str(r.status_code))