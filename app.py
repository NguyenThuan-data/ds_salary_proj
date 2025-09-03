from flask import Flask, render_template, jsonify, abort, request
import os
import re
import math
import pandas as pd

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILES = {
    'DataScientist.csv': os.path.join(BASE_DIR, 'DataScientist.csv'),
    'data_eda.csv': os.path.join(BASE_DIR, 'data_eda.csv'),
    'Salary_data_cleaned.csv': os.path.join(BASE_DIR, 'Salary_data_cleaned.csv'),
}

# ---- Data loading and normalization ---------------------------------------

def _existing_data_path():
    for name in ['data_eda.csv', 'Salary_data_cleaned.csv', 'DataScientist.csv']:
        p = DATA_FILES.get(name)
        if p and os.path.exists(p):
            return p
    return None


def _normalize_columns(df: pd.DataFrame) -> dict:
    mapping = {}
    for c in df.columns:
        key = re.sub(r"\s+", " ", str(c).strip()).lower()
        mapping[key] = c
    return mapping


def _ensure_salary_column(df: pd.DataFrame, colmap: dict) -> str:
    # Prefer provided average columns
    for k in ['avr salary', 'avr_salary', 'average salary', 'avg salary', 'salary_avg', 'avr']:
        if k in colmap:
            return colmap[k]
    # Compute from min/max when available
    min_names = [n for n in ['min salary', 'min_salary', 'salary_min'] if n in colmap]
    max_names = [n for n in ['max salary', 'max_salary', 'salary_max'] if n in colmap]
    if min_names and max_names:
        df['__salary_avg__'] = (pd.to_numeric(df[colmap[min_names[0]]], errors='coerce') +
                                 pd.to_numeric(df[colmap[max_names[0]]], errors='coerce')) / 2.0
        return '__salary_avg__'
    # Parse from raw estimate when present
    if 'salary estimate' in colmap:
        raw = df[colmap['salary estimate']].astype(str)
        # drop entries marked -1
        raw = raw[raw.str.strip() != '-1']
        nums = raw.str.extract(r"(?i)(\$?\s*([0-9]{2,3})\s*K)\s*-\s*(\$?\s*([0-9]{2,3})\s*K)")
        # Fallback single value
        single = raw.str.extract(r"(?i)(\$?\s*([0-9]{2,3})\s*K)")
        minv = pd.to_numeric(nums[1].fillna(single[1]), errors='coerce')
        maxv = pd.to_numeric(nums[3].fillna(single[1]), errors='coerce')
        df['__salary_avg__'] = (minv + maxv) * 500  # convert K-range avg
        return '__salary_avg__'
    raise ValueError('Could not determine salary column')


def _dataset_and_meta():
    path = _existing_data_path()
    if not path:
        return None, {}
    df = pd.read_csv(path, low_memory=False)
    colmap = _normalize_columns(df)
    # Compute/identify salary column
    try:
        sal_col = _ensure_salary_column(df, colmap)
    except Exception:
        sal_col = None
    # Build available filters dynamically
    options = {}
    for key, label in [
        ('job_state', 'Location (State)'),
        ('job_simp', 'Job Title'),
        ('industry', 'Industry'),
        ('sector', 'Sector'),
        ('senority', 'Seniority'),
        ('seniority', 'Seniority'),
    ]:
        if key in colmap:
            series = df[colmap[key]].dropna().astype(str)
            options[key] = sorted(series.unique().tolist())[:200]
    # Skill flags
    skills = []
    for flag, nice in [('python_yn', 'Python'), ('spark', 'Spark'), ('aws', 'AWS'), ('excel', 'Excel'), ('rstudio_yn', 'R Studio')]:
        if flag in colmap:
            skills.append({'key': flag, 'label': nice})
    meta = {
        'path': path,
        'colmap': colmap,
        'salary_col': sal_col,
        'options': options,
        'skills': skills,
    }
    return df, meta


# ---- Web UI ---------------------------------------------------------------

@app.route('/')
@app.route('/explore')
def explore():
    df, meta = _dataset_and_meta()
    if df is None:
        files = [name for name, path in DATA_FILES.items() if os.path.exists(path)]
        return render_template('index.html', files=files, meta={})
    # Read filters from query
    args = request.args
    colmap = meta['colmap']
    working = df.copy()
    # Apply categorical filters if present
    for key in meta['options'].keys():
        val = args.get(key)
        if val and key in colmap:
            working = working[working[colmap[key]].astype(str) == val]
    # Apply skill flags
    for s in meta['skills']:
        if args.get(s['key']) == '1' and s['key'] in colmap:
            working = working[working[colmap[s['key']]] == 1]
    # Compute summary
    salary_col = meta['salary_col']
    summary = None
    top_breakdowns = {}
    if salary_col and not working.empty:
        vals = pd.to_numeric(working[salary_col], errors='coerce').dropna()
        if not vals.empty:
            summary = {
                'count': int(vals.shape[0]),
                'avg': round(float(vals.mean()), 2),
                'median': round(float(vals.median()), 2),
                'p25': round(float(vals.quantile(0.25)), 2),
                'p75': round(float(vals.quantile(0.75)), 2),
                'min': round(float(vals.min()), 2),
                'max': round(float(vals.max()), 2),
            }
            # Breakdown by state and title if present
            for key in ['job_state', 'job_simp', 'industry']:
                if key in colmap:
                    g = working.groupby(working[colmap[key]].astype(str))[salary_col].mean().sort_values(ascending=False).head(10)
                    top_breakdowns[key] = g.round(2).reset_index().values.tolist()
    return render_template(
        'index.html',
        files=[],
        meta=meta,
        summary=summary,
        top_breakdowns=top_breakdowns,
        selected=args
    )


# ---- JSON APIs ------------------------------------------------------------

@app.route('/api/preview/<path:fname>')
def preview(fname: str):
    file_path = DATA_FILES.get(fname)
    if not file_path or not os.path.exists(file_path):
        abort(404)
    try:
        df = pd.read_csv(file_path, nrows=50)
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
        df = pd.read_csv(file_path, nrows=5)
        return jsonify({'file': fname, 'columns': list(df.columns.astype(str).values)})
    except Exception as e:
        abort(500, description=str(e))


@app.route('/api/estimate')
def estimate():
    df, meta = _dataset_and_meta()
    if df is None or not meta.get('salary_col'):
        abort(503)
    working = df.copy()
    colmap = meta['colmap']
    for key in meta['options'].keys():
        val = request.args.get(key)
        if val and key in colmap:
            working = working[working[colmap[key]].astype(str) == val]
    for s in meta['skills']:
        if request.args.get(s['key']) == '1' and s['key'] in colmap:
            working = working[working[colmap[s['key']]] == 1]
    vals = pd.to_numeric(working[meta['salary_col']], errors='coerce').dropna()
    if vals.empty:
        return jsonify({'count': 0, 'avg': None})
    return jsonify({'count': int(vals.shape[0]), 'avg': round(float(vals.mean()), 2)})


@app.route('/health')
def health():
    return jsonify({'ok': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
