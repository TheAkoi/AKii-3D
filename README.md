# Quick Manual: AK!i 3D

## Purpose
AK!i 3D Predicts drug release over time from 3D-printed tablets using input data on drug properties, formulation composition and geometry, and printing settings.

## Installation
To get the Flask application running, make sure you have downloaded everything from this repository, and save the files in a defined location. 

First, start by confirming that you have `Python 3.8 or newer installed, Running` ***`python --version`*** in your terminal will show the version. 

Next, it’s best practice to work inside a dedicated virtual environment: run ***`python -m venv venv`***, 

After that, activate the environment with ***`source venv/bin/activate`*** on macOS / Linux or ***`venv\Scripts\activate`*** on Windows. 

Once the environment is active, change the directory to the location where you have the files downloaded. 

Then, install the project’s dependencies by executing ***`pip install -r requirements.txt`***; this pulls in Flask, pandas, scikit-learn, LightGBM, and the other libraries listed in the requirements.txt file.

Before launching the server, make sure the essential files, ***`LightGBM_Best_model_full.pkl`,  `New_scaler_full.pkl`, and `New_full_features.json`***, are in the same directory as ***`app.py`***. These files contain the trained model, its associated scaler, and the feature list; without them the prediction routes will raise errors.

With the prerequisites satisfied, start the application simply by running ***python app.py***. 

Flask will boot in development mode, binding by default to `http://127.0.0.1:5000/`. When you visit that address in a browser, you’ll see a form where you can either upload a CSV or enter feature values manually. 

## Steps to Use
### Step 1: Enter or Load the Data
•	Fill in API properties (e.g., MW, LogP, Solubility).
•	Enter formulation components (% of each excipient).
•	Input 3D printing parameters and tablet dimensions.

### Step 2: Set Timepoints
•	Example: 5, 10, 15 (in minutes).

### Step 3: Get Predictions
•	Click “Predict” to see the release% over time.

### Step 4: Visualize and Download Results 
•	Use “Download CSV/XLSX”.
•	Checkbox Option to include input data.
 
# Notes:
•	Use “Fill with Example” to see the format.

•	Or upload a CSV with your data.

•	All numeric fields must be valid, and the composition sum must not exceed 100%.


## You can Cite this work [Here](.com)
