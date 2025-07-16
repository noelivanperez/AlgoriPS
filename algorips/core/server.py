from flask import Flask, Response
from prometheus_client import generate_latest, Counter

app = Flask(__name__)
REQUESTS = Counter('algorips_requests_total', 'Total requests')

@app.route('/healthz')
def healthz():
    return 'ok'

@app.route('/metrics')
def metrics():
    REQUESTS.inc()
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
