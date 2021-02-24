from flask import Flask, jsonify
import logging

#app = Flask(__name__)

app = Flask('Code Challenge Backend Service')
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
LOG = app.logger

@app.route('/', methods=['GET'])
def home():
    LOG.info('{} method called'.format(__name__))
    return jsonify({"message" :"Processed by the backend service!"})

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5001)
