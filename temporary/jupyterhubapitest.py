import requests

token = 'c953fddddaeb43d4a1d55d4236f4f063'
api_url = 'http://47.96.41.8:2345/hub/api'

data = {'usernames': ['ecust'], 'admin':False}

r = requests.post(api_url + '/users',
    headers={
             'Authorization': 'token %s' % token,
            },
    json=data
)
r.raise_for_status()
r.json()

r = requests.get(api_url + '/users',
    headers={
             'Authorization': 'token %s' % token,
            }
    )

r.raise_for_status()
users = r.json()
print(users)

