# from flask import Flask, jsonify, request
# from time import sleep

# app = Flask(__name__)

# @app.route('/flask/api', methods=['POST'])
# def api():
#     sleep(3)

#     print(request.json)

#     return jsonify({'message': 'successful.'})


# if __name__ == '__main__':
#     app.run(port=5050)


# import requests, json

# url = f"http://54.179.47.77:1337/test-cams/61b962d05316b205787eaa89"

# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxYjQwZDVjMjY4ZjBkMDE5YzljMGU3ZCIsImlhdCI6MTYzOTUzODQxMywiZXhwIjoxNjQyMTMwNDEzfQ.D2b9OYJJJCd0fJEaf1eKnJjgtC5owmtsC6GLuEAUxa4",
#     "Content-Type": "application/json"
#     }
# # body = json.dumps({"count": 9})
# body = {"count": 9}

# response = requests.put(url, headers=headers, json=body)

# print(response.status_code)
# print(response.json())


# import datetime

# def time_in_range(start, end, current):
#     """Returns whether current is in the range [start, end]"""
#     return start <= current <= end


# start = datetime.time(0, 0, 0)
# end = datetime.time(23, 55, 0)
# current = datetime.datetime.now().time()

# print(time_in_range(start, end, current))
# True (if you're not a night owl) ;)


# from flask import Flask, request

# app = Flask(__name__)

# @app.route('/', methods=['POST'])
# def index():
#     json = request.json
#     print(json)

#     return "Hello, World"

# app.run(port=1234)

import requests

url = "https://0857-58-136-2-49.ngrok.io/occupation-histories"

json = {
    "time": "21:46:51",
    "day": "Monday",
    "in_count": 0,
    "out_count": 0,
    "occupation": "61f0d5d43cd3e300af0e957a"
}

response = requests.post(url, data = json)

print(response)
