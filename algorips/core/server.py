from flask import Flask, Response, jsonify, request
from prometheus_client import generate_latest, Counter, Summary
import time
from .analyzer import CodeAnalyzer
from .db_connector import execute_query
from .ollama_client import OllamaClient

app = Flask(__name__)
REQUESTS = Counter('algorips_requests_total', 'Total requests')
ANALYSIS_COUNT = Counter('algorips_analysis_total', 'Total analyses')
ANALYSIS_LATENCY = Summary('algorips_analysis_latency_seconds', 'Analysis latency seconds')
client = OllamaClient()

@app.route('/healthz')
def healthz():
    return 'ok'

@app.route('/metrics')
def metrics():
    REQUESTS.inc()
    return Response(generate_latest(), mimetype='text/plain')


@app.route('/analyze')
def analyze_route():
    """Run analysis on a given path query parameter"""
    path = request.args.get('path', '.')
    start = time.perf_counter()
    result = CodeAnalyzer().scan(path)
    duration = time.perf_counter() - start
    ANALYSIS_COUNT.inc()
    ANALYSIS_LATENCY.observe(duration)
    return jsonify(result)


@app.route('/chat', methods=['POST'])
def chat_route():
    """Forward chat prompts to the Ollama client."""
    data = request.get_json() or {}
    prompt = data.get('prompt', '')
    result = client.send_prompt(prompt)
    return jsonify(result)


@app.route('/db/query', methods=['POST'])
def db_query_route():
    """Run a parameterized SQL query using stored credentials."""
    data = request.get_json(force=True) or {}
    name = data.get('name')
    sql = data.get('sql')
    params = data.get('params') or {}
    if not name or not sql:
        return jsonify({'error': 'name and sql required'}), 400
    rows = execute_query(name, sql, params)
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
