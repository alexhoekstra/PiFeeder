'''
 Unimplemented web service for PiFeeder
 TODO: Add a switch feed times and a option for web camera
 @author Alex Hoekstra
'''
from flask import Flask

app = Flask(__name__)
@app.route("/")
def hello():
  return "Hello World!"
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80, debug=True)