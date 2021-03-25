import requests
import json

code = "C000117"
query = 'mq2_pcourse.code: \"'+code+'\"'
url = "https://coursehandbook.mq.edu.au/api/es/search"
courses = {"query":{"bool":{"must":[{"query_string":{"query":query}},{"term":{"live":"true"}}]}},"aggs":{"implementationYear":{"terms":{"field":"mq2_pcourse.implementationYear_dotraw","size":100}},"availableInYears":{"terms":{"field":"mq2_pcourse.availableInYears_dotraw","size":100}}},"size":100,"_source":{"includes":["versionNumber","availableInYears","implementationYear"]}}
headers = {'content-type': 'application/json'}

formatted = {}

r = requests.post(url, data=json.dumps(courses), headers=headers)
if r.status_code == 200:
    output = r.json()
    contentlets = output.get('contentlets')
    for i in range(len(contentlets)):
        data = contentlets[i].get('data')
        parsed = json.loads(data)

        with open('data/indivCourse'+str(i)+'.json', 'w') as outfile:
            json.dump(parsed, outfile, indent=4, sort_keys=True)
else:
    print("Error encountered: "+str(r.status_code))