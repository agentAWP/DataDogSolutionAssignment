from flask import Flask
import logging
import sys
from ddtrace import tracer,config

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
#Service and resource parameters added
@tracer.wrap("flask.request", service='flask_app', resource='APM', span_type="web")
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
#Service and resource parameters added
@tracer.wrap("flask.request", service='flask_app', resource='TRACE', span_type="web")
def trace_endpoint():
	return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
