from flask import Flask, render_template, jsonify, abort
import os
import pandas as pd

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Whitelist of data files available in the repo
DATA_FILES = {
    'DataScientist.csv': os.path.join(BASE_DIR, 'DataScientist.csv'),
    'data_eda.csv': os.path.join(BASE_DIR, 'data_eda.csv'),
    'Salary_data_cleaned.csv': os.path.join(BASE_DIR, 'Salary_data_cleaned.csv'),
}

@app.route('/')
def index():
    # Show a simple index with available datasets and basic actions
    files = [name for name, path in DATA_FILES.items() if os.path.exists(path)]
    return render_template('index.html', files=files)

@app.route('/api/preview/<path:fname>')
def preview(fname: str):
    # Return a small preview of a dataset as JSON
    file_path = DATA_FILES.get(fname)
    if not file_path or not os.path.exists(file_path):
        abort(404)
    try:
        # Try CSV preview
        df = pd.read_csv(file_path, nrows=50)
        # Convert to records (limited to first 10 rows for payload size)
        records = df.head(10).to_dict(orient='records')
        summary = {
            'rows': int(df.shape[0]),
            'cols': int(df.shape[1]),
            'columns': list(df.columns.astype(str).values),
        }
        return jsonify({'file': fname, 'summary': summary, 'sample': records})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/api/columns/<path:fname>')
def columns(fname: str):
    file_path = DATA_FILES.get(fname)
    if not file_path or not os.path.exists(file_path):
        abort(404)
    try:
        # Read a small chunk just to infer columns
        df = pd.read_csv(file_path, nrows=5)
        return jsonify({'file': fname, 'columns': list(df.columns.astype(str).values)})
    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    # Bind to 0.0.0.0 and port 3000 for the platform proxy
    app.run(host='0.0.0.0', port=3000, debug=False)
