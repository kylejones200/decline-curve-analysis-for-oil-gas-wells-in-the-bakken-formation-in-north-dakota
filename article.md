# Decline Curve Analysis for Oil & Gas Wells in the Bakken Formation in North Dakota Decline curve analysis is a technique in petroleum engineering used to
predict how wells will produce over time. This approach helps...

### Decline Curve Analysis for Oil & Gas Wells in the Bakken Formation in North Dakota
Decline curve analysis is a technique in petroleum engineering used to
predict how wells will produce over time. This approach helps operators
and investors understand which companies are managing their assets most
effectively. Using publicly available production data from the State of
North Dakota, we can fit mathematical models to well output and rank
operators based on their long-term production potential.


<figcaption>Photo by <a
href="https://unsplash.com/@neganova?utm_source=medium&amp;utm_medium=referral"
class="markup--anchor markup--figure-anchor"
data-href="https://unsplash.com/@neganova?utm_source=medium&amp;utm_medium=referral"
rel="photo-creator noopener" target="_blank">Valeriia Neganova</a> on <a
href="https://unsplash.com?utm_source=medium&amp;utm_medium=referral"
class="markup--anchor markup--figure-anchor"
data-href="https://unsplash.com?utm_source=medium&amp;utm_medium=referral"
rel="photo-source noopener" target="_blank">Unsplash</a></figcaption>


Our analysis began with data from the North Dakota Monthly Production
Report Index. This dataset provides well-level production statistics,
including oil, gas, and water output, as well as details on well
operators. Since our objective was to assess production trends across
operators, we first structured the data by extracting relevant fields,
converting date formats, and aggregating monthly production figures.
Given that our data started in January 2016, we did not have the true
initial production rates for many wells. Instead, we worked with
available data to fit decline curves based on observed production
trends.

```python
import requests
import os
from time import sleep
# Base URL pattern
base_url = "https://www.dmr.nd.gov/oilgas/mpr/{year}_{month}.xlsx"

# Set the range of years and months
start_year = 2016
end_year = 2024  # Adjust this to the latest available year

# Folder to save downloaded files
download_folder = "dmr_mpr_files"
os.makedirs(download_folder, exist_ok=True)

# Loop through years and months
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        # Format month as two digits
        month_str = f"{month:02d}"
        file_url = base_url.format(year=year, month=month_str)
        file_name = f"{year}_{month_str}.xlsx"
        file_path = os.path.join(download_folder, file_name)

        # Check if file already exists (skip if downloaded)
        if os.path.exists(file_path):
            print(f"Skipping {file_name}, already downloaded.")
            continue

        print(f"Downloading {file_url}...")

        try:
            response = requests.get(file_url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                print(f"✔ Downloaded: {file_name}")
            else:
                print(f"❌ Failed: {file_name} (Status {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"⚠ Error downloading {file_name}: {e}")

        # Sleep to avoid overwhelming the server
        sleep(1)

print("✅ Download process complete.")

output_csv = "merged_mpr_data.csv"

# List all .xlsx files in the folder
xlsx_files = [f for f in os.listdir(download_folder) if f.endswith(".xlsx")]

# Check if there are any files to process
if not xlsx_files:
    print("No Excel files found in the folder.")
else:
    print(f"Found {len(xlsx_files)} files. Merging...")

    # List to store dataframes
    dataframes = []

    # Read and merge each Excel file
    for file in sorted(xlsx_files):  # Sorting ensures chronological order
        file_path = os.path.join(download_folder, file)
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            df["Source_File"] = file  # Add a column to track file origins
            dataframes.append(df)
            print(f"✔ Processed: {file}")
        except Exception as e:
            print(f"❌ Failed to read {file}: {e}")

    # Concatenate all dataframes
    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)

        # Save to CSV
        merged_df.to_csv(output_csv, index=False)
        print(f"✅ Merged file saved as {output_csv}")
    else:
        print("No valid data to merge.")
```

To model decline behavior, we chose the hyperbolic decline model which
captures gradual slowdowns typical of unconventional wells. This model
accounts for a higher initial drop-off followed by a more stable
production period than exponential decline, making it well-suited for
the Bakken's shale oil formations. The hyperbolic equation relies on
three parameters: an estimated initial production rate, an initial
decline rate, and a b-factor, which governs how decline slows over time.
We fit this model to each well's monthly production data and derived
these parameters for each well that has at least five months of
production.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Load the combined dataset
df = pd.read_csv("merged_mpr_data.csv")  # or merged_mpr_data_pdf.csv

# Convert date-related fields
df["Year"] = df["Source_File"].str.extract(r"(\d{4})").astype(int)
df["Month"] = df["Source_File"].str.extract(r"_(\d{2})").astype(int)

# Create a datetime column
df["Date"] = pd.to_datetime(df[["Year", "Month"]].assign(day=1))

# Drop unnecessary columns
df = df.drop(columns=["Source_File"])

# Convert numeric fields
numeric_columns = ["Oil", "Wtr", "Days", "Runs", "Gas", "GasSold"]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")

# Group by well and sum production for each month
well_production = df.groupby(["WellName", "Date"]).agg({
    "Oil": "sum",
    "Gas": "sum",
    "Wtr": "sum"
}).reset_index()

# Define the hyperbolic decline function
def hyperbolic_decline(t, q_i, D_i, b):
    return q_i / ((1 + b * D_i * t) ** (1 / b))

# Select a sample well
well_name = "AMBER ELIZABETH  36-25H"
well_data = well_production[well_production["WellName"] == well_name].sort_values("Date")

# Convert dates to months since 2016-01-01
well_data = well_data[well_data["Date"] >= "2016-01-01"]
well_data["Months"] = (well_data["Date"] - pd.Timestamp("2016-01-01")).dt.days / 30.0

t = well_data["Months"].values
q = well_data["Oil"].values

# Fit the hyperbolic decline curve
try:
    popt, _ = curve_fit(hyperbolic_decline, t, q, maxfev=10000, bounds=([0, 0, 0], [np.inf, 1, 2]))
    q_i, D_i, b = popt
except:
    print(f"Error in fitting for {well_name}")
    q_i, D_i, b = None, None, None

# Predict production decline
t_future = np.linspace(0, 120, 120)  # Predict for 10 years
q_future = hyperbolic_decline(t_future, q_i, D_i, b)

# Plot the actual vs. predicted production
plt.figure(figsize=(10,5))
plt.scatter(t, q, label="Actual Production", color="blue")
plt.plot(t_future, q_future, label="Hyperbolic Decline Fit", color="red")
plt.xlabel("Months Since 2016-01-01")
plt.ylabel("Oil Production (BBL)")
plt.title(f"Hyperbolic Decline Fit for {well_name}")
plt.legend()
plt.show()
```


<figcaption>Example of one well with DCA</figcaption>


``` 
# Print the estimated parameters
print(f"Estimated Initial Production (q_i): {q_i:.2f} BBL")
print(f"Estimated Initial Decline Rate (D_i): {D_i:.4f} per month")
print(f"Estimated b-Factor: {b:.4f}")

# Perform hyperbolic decline curve fitting for all wells
decline_results = []

for well in well_production["WellName"].unique():
    well_data = well_production[well_production["WellName"] == well].sort_values("Date")
    well_data = well_data[well_data["Date"] >= "2016-01-01"]
    
    # Convert date to months since 2016-01-01
    well_data["Months"] = (well_data["Date"] - pd.Timestamp("2016-01-01")).dt.days / 30.0
    t = well_data["Months"].values
    q = well_data["Oil"].values

    if len(t) < 5:  # Need enough data points to fit
        continue

    try:
        popt, _ = curve_fit(hyperbolic_decline, t, q, maxfev=10000, bounds=([0, 0, 0], [np.inf, 1, 2]))
        q_i, D_i, b = popt
        decline_results.append({"WellName": well, "q_i": q_i, "D_i": D_i, "b": b})
    except:
        print(f"Skipping {well} (error in fitting)")

# Convert to DataFrame
df_decline = pd.DataFrame(decline_results)

# Save results
df_decline.to_csv("hyperbolic_decline_results.csv", index=False)
print("Decline curve analysis saved to hyperbolic_decline_results.csv")

# Compute Estimated Ultimate Recovery (EUR)
df_decline["EUR"] = df_decline["q_i"] / df_decline["D_i"]
df_decline.to_csv("hyperbolic_decline_results_with_EUR.csv", index=False)

# Display top wells by decline rate
print(df_decline.sort_values("D_i", ascending=False).head(10))
```

With the decline curves for individual wells calculated (41,527 wells!),
the next step was to evaluate operator performance. This required
associating each well with its operator and aggregating results at the
company level.

Inconsistencies in operator names --- such as variations in
capitalization and punctuation --- posed a challenge. To address this,
we standardized all operator names by converting them to uppercase and
removing punctuation. This step ensured that wells belonging to the same
company were correctly grouped together.

```python
import pandas as pd
import numpy as np
import string

# Load decline curve analysis results
df_decline = pd.read_csv("hyperbolic_decline_results_with_EUR.csv")

# Load the original dataset to get operator names
df = pd.read_csv("merged_mpr_data.csv")

# Extract well-to-operator mapping
well_operator_map = df[["WellName", "Operator"]].drop_duplicates()

# Standardize operator names: capitalize and remove punctuation
def clean_operator_name(name):
    return name.translate(str.maketrans("", "", string.punctuation)).upper().strip()

well_operator_map["Operator"] = well_operator_map["Operator"].astype(str).apply(clean_operator_name)

# Merge operator names into the decline curve results
df_decline = df_decline.merge(well_operator_map, on="WellName", how="left")

# Drop wells without an associated operator (if any)
df_decline = df_decline.dropna(subset=["Operator"])

# Aggregate results by operator
df_operator = df_decline.groupby("Operator").agg({
    "q_i": "mean",  # Average initial production rate
    "D_i": "mean",  # Average decline rate
    "b": "mean",    # Average b-factor
    "EUR": "sum"    # Total Estimated Ultimate Recovery (EUR) per operator
}).reset_index()

# Rank operators based on EUR
df_operator = df_operator.sort_values("EUR", ascending=False)

# Display top 10 best-performing operators (highest EUR)
print("🏆 Top 10 Best Operators (Highest EUR):")
print(df_operator.head(10))

# Display bottom 10 worst-performing operators (lowest EUR)
print("\n❌ Bottom 10 Worst Operators (Lowest EUR):")
print(df_operator.tail(10))

# Save results
df_operator.to_csv("operator_performance_ranking.csv", index=False)
print("Operator performance ranking saved to operator_performance_ranking.csv")
```

Then, we computed aggregate performance metrics for each company using
Estimated Ultimate Recovery (EUR), which represents the total
recoverable oil a well or operator is expected to produce over its
lifetime. By summing EUR values across wells, we identified the best
(and worst) performing operators in the Bakken since 2016 from 233
unique operators.


This approach offers insights for operators, investors, and policymakers
seeking to understand production trends in the Bakken.
::::::::By [Kyle Jones](https://medium.com/@kyle-t-jones) on
[February 12, 2025](https://medium.com/p/ce4cbccb91e8).

[Canonical
link](https://medium.com/@kyle-t-jones/decline-curve-analysis-for-oil-gas-wells-in-the-bakken-formation-in-north-dakota-ce4cbccb91e8)

Exported from [Medium](https://medium.com) on November 10, 2025.
