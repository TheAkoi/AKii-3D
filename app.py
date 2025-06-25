from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import joblib
import json
import os

app = Flask(__name__)

# Load model and preprocessing
model = joblib.load('LightGBM_Best_model_full.pkl')
scaler = joblib.load('New_scaler_full.pkl')
with open('New_full_features.json') as f:
    important_features = json.load(f)

DOWNLOAD_DF = None
FEATURES = important_features

def preprocess_and_predict(raw_df):
    X_scaled = scaler.transform(raw_df)
    mask = [f in important_features for f in raw_df.columns]
    X_selected = X_scaled[:, mask]
    preds = model.predict(X_selected)
    return preds

@app.route('/')
def index():
    return render_template('form.html', features=FEATURES)

@app.route('/load', methods=['POST'])
def load_csv():
    form_values = {}
    include_inputs = "include_inputs" in request.form

    csv_file = request.files.get("csv_file")
    if csv_file:
        try:
            df = pd.read_csv(csv_file)
            if df.shape[0] == 0:
                raise ValueError("CSV is empty.")
            row = df.iloc[0].to_dict()
            form_values = {str(k): v for k, v in row.items()}
        except Exception as e:
            return render_template("form.html", features=FEATURES, error=f"Error loading CSV: {e}", form_values={}, include_inputs=include_inputs)

    return render_template("form.html", features=FEATURES, form_values=form_values, include_inputs=include_inputs)

@app.route('/predict', methods=['POST'])
def predict():
    global DOWNLOAD_DF
    try:
        include_inputs = 'include_inputs' in request.form
        file = request.files.get('csv_file')
        predictions = []

        if file and file.filename:
            df = pd.read_csv(file)
            preds = preprocess_and_predict(df)
            df['Predicted Release %'] = preds
            DOWNLOAD_DF = df if include_inputs else df[['Time(mins)', 'Predicted Release %']]
            predictions = list(zip(df.get('Time(mins)', range(len(df))), preds.tolist()))
        else:
            form_data = request.form.to_dict()
            form_data.pop('include_inputs', None)
            times_str = form_data.pop('Time(mins)', '')
            times = [float(t.strip()) for t in times_str.replace(',', ' ').split() if t.strip()]
            rows = []
            for t in times:
                row = form_data.copy()
                row['Time(mins)'] = t
                rows.append(row)

            df = pd.DataFrame(rows, dtype=float)
            preds = preprocess_and_predict(df)
            df['Predicted Release %'] = preds
            DOWNLOAD_DF = df if include_inputs else df[['Time(mins)', 'Predicted Release %']]
            predictions = list(zip(times, preds.tolist()))

        return render_template(
            'form.html',
            features=FEATURES,
            predictions=predictions,
            show_download=True,
            include_inputs=include_inputs
        )

    except Exception as e:
        return render_template('form.html', features=FEATURES, error=str(e))

@app.route('/download/<fmt>')
def download(fmt):
    global DOWNLOAD_DF
    if DOWNLOAD_DF is None:
        return "No data available to download.", 400

    if fmt == 'csv':
        path = 'predictions.csv'
        DOWNLOAD_DF.to_csv(path, index=False)
    elif fmt == 'xlsx':
        path = 'predictions.xlsx'
        DOWNLOAD_DF.to_excel(path, index=False)
    else:
        return "Unsupported format", 400

    return send_file(path, as_attachment=True)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.json
    df = pd.DataFrame(data)
    preds = preprocess_and_predict(df)
    return jsonify({'predictions': preds.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
