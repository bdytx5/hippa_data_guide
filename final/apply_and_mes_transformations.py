

import pandas as pd
import numpy as np
from itertools import combinations
import wandb

# Initialize W&B project
wandb.init(project="data_de-identification", name="transformation_metrics_logging")

# Load the medical dataset, specifying data types
dtype_spec = {
    'ZIP_code': str,
    'Birth_date': str,
    'Gender': str,
    'Total_charge': str,  # Ensure that 'Total_charge' is read as a string initially
    'Diagnosis': str
}

# Load medical data
medical_data_original = pd.read_csv('synthetic_medical_data_with_governor.csv', dtype=dtype_spec)
medical_data = medical_data_original.copy()

# Define the possible transformations
def generalize_birth_to_year(data):
    data['Birth_date'] = pd.to_datetime(data['Birth_date'], errors='coerce').dt.year.astype(str)
    return data

def generalize_birth_to_age_range(data, bin_size=10):
    data['Birth_date'] = pd.to_datetime(data['Birth_date'], errors='coerce')
    current_year = pd.Timestamp.now().year
    data['Birth_date'] = current_year - data['Birth_date'].dt.year  # Calculate age
    data['Birth_date'] = data['Birth_date'].fillna(0).astype(int)
    data['Birth_date'] = ((data['Birth_date'] // bin_size) * bin_size).astype(str) + '-' + \
                         ((data['Birth_date'] // bin_size) * bin_size + bin_size - 1).astype(str)
    return data

def generalize_zip_code_prefix(data, prefix_length=3):
    data['ZIP_code'] = data['ZIP_code'].astype(str)
    data['ZIP_code'] = data['ZIP_code'].str[:prefix_length]
    return data

def suppress_gender(data):
    data['Gender'] = 'Suppressed'
    return data

def bin_total_charge(data, bin_size=1000):
    if 'Total_charge' in data.columns:
        data['Total_charge'] = pd.to_numeric(data['Total_charge'], errors='coerce').fillna(0).astype(int)
        data['Total_charge'] = (data['Total_charge'] // bin_size) * bin_size
        data['Total_charge'] = data['Total_charge'].astype(str) + '-' + \
                               (data['Total_charge'] + bin_size - 1).astype(str)
    return data

def top_bottom_code_total_charge(data, top_threshold=9000, bottom_threshold=1000):
    if 'Total_charge' in data.columns:
        data['Total_charge'] = pd.to_numeric(data['Total_charge'], errors='coerce').fillna(0).astype(int)
        data['Total_charge'] = data['Total_charge'].clip(lower=bottom_threshold, upper=top_threshold)
    return data

def redact_rare_diagnoses(data, threshold=5):
    if 'Diagnosis' in data.columns:
        diagnosis_counts = data['Diagnosis'].value_counts()
        rare_diagnoses = diagnosis_counts[diagnosis_counts < threshold].index
        data.loc[data['Diagnosis'].isin(rare_diagnoses), 'Diagnosis'] = 'Other'
    return data

# List of transformation functions
transformations = [
    ('Generalize Birth Date to Year', generalize_birth_to_year),
    ('Generalize Birth Date to Age Range', generalize_birth_to_age_range),
    ('Generalize ZIP Code to Prefix', generalize_zip_code_prefix),
    ('Suppress Gender', suppress_gender),
    ('Bin Total Charge', bin_total_charge),
    ('Top/Bottom Code Total Charge', top_bottom_code_total_charge),
    ('Redact Rare Diagnoses', redact_rare_diagnoses)
]

# Functions to calculate privacy metrics
def calculate_k_anonymity(data, quasi_identifiers):
    grouped = data.groupby(quasi_identifiers)
    group_sizes = grouped.size()
    return group_sizes.min()

def calculate_l_diversity(data, quasi_identifiers, sensitive_attribute):
    grouped = data.groupby(quasi_identifiers)
    return grouped[sensitive_attribute].nunique().min()

def calculate_t_closeness(data, quasi_identifiers, sensitive_attribute):
    overall_distribution = data[sensitive_attribute].value_counts(normalize=True)
    grouped = data.groupby(quasi_identifiers)
    max_t = 0
    for _, group in grouped:
        group_distribution = group[sensitive_attribute].value_counts(normalize=True)
        t_distance = abs(overall_distribution - group_distribution).sum() / 2
        max_t = max(max_t, t_distance)
    return max_t

# Function to apply transformations and calculate privacy metrics
def apply_transformations_and_evaluate(transform_list, target_k=None, target_l=None, target_t=None, min_thresholds=False):
    data = medical_data.copy()
    description = ''
    for name, func in transform_list:
        data = func(data)
        description += f'{name}, '

    if 'Diagnosis' in data.columns:
        data['Diagnosis'] = data['Diagnosis'].fillna('Unknown')

    quasi_identifiers = [col for col in ['ZIP_code', 'Birth_date', 'Gender'] if col in data.columns]

    k_anonymity = calculate_k_anonymity(data, quasi_identifiers)
    l_diversity = calculate_l_diversity(data, quasi_identifiers, 'Diagnosis')
    t_closeness = calculate_t_closeness(data, quasi_identifiers, 'Diagnosis')

    k_error = abs(target_k - k_anonymity) if target_k is not None else 0
    l_error = abs(target_l - l_diversity) if target_l is not None else 0
    t_error = abs(target_t - t_closeness) if target_t is not None else 0

    if min_thresholds:
        if target_k is not None and k_anonymity < target_k:
            return None, None
        if target_l is not None and l_diversity < target_l:
            return None, None
        if target_t is not None and t_closeness > target_t:
            return None, None

    total_error = k_error + l_error + t_error

    return data, {
        'Transformations Applied': description.strip(', '),
        'Quasi-Identifiers': quasi_identifiers,
        'K-Anonymity': k_anonymity,
        'L-Diversity': l_diversity,
        'T-Closeness': t_closeness,
        'Total Error': total_error
    }

# Apply transformations and evaluate
results = []
for transformation in transformations:
    _, result = apply_transformations_and_evaluate([transformation], target_k=5, target_l=3, target_t=0.15)
    if result:
        results.append(result)

# Apply combinations of transformations
for r in range(2, len(transformations) + 1):
    comb_list = list(combinations(transformations, r))
    for comb in comb_list:
        _, result = apply_transformations_and_evaluate(comb, target_k=5, target_l=3, target_t=0.15)
        if result:
            results.append(result)

# Sort and display the results
results = sorted(results, key=lambda x: x['Total Error'])
print(f"\nTransformations sorted by closeness to desired k-anonymity, l-diversity, and t-closeness values:")
for result in results:
    print(f"Transformations Applied: {result['Transformations Applied']}")
    print(f"Quasi-Identifiers: {result['Quasi-Identifiers']}")
    print(f"K-Anonymity: {result['K-Anonymity']}, L-Diversity: {result['L-Diversity']}, T-Closeness: {result['T-Closeness']:.4f}")
    print(f"Total Error: {result['Total Error']}\n")

# Create a W&B Table to log the results
table = wandb.Table(columns=["Transformations Applied", "Quasi-Identifiers", "K-Anonymity", "L-Diversity", "T-Closeness", "Total Error"])

# Populate the W&B Table with transformation results
for result in results:
    table.add_data(
        result['Transformations Applied'],
        str(result['Quasi-Identifiers']),
        result['K-Anonymity'],
        result['L-Diversity'],
        result['T-Closeness'],
        result['Total Error']
    )

# Log the table to W&B
wandb.log({"Transformation Metrics": table})

# Prompt user to select transformations
print("Available transformations:")
for idx, (name, _) in enumerate(transformations, start=1):
    print(f"{idx}. {name}")

selected_indices = input("Select transformations to apply by entering their numbers separated by commas (e.g., 1,3,5): ")
selected_indices = [int(i.strip()) for i in selected_indices.split(',') if i.strip().isdigit()]

# Get the list of selected transformations
selected_transformations = [transformations[i-1] for i in selected_indices]

# Apply the selected transformations to the data and get modified data with metrics
modified_data, modified_data_metrics = apply_transformations_and_evaluate(selected_transformations, target_k=5, target_l=3, target_t=0.15)

# Save the modified data to a new file
modified_data.to_csv('modified_data.csv', index=False)
print("Modified data saved to 'modified_data.csv'.")

# Re-read the saved modified data for verification
modified_data_reloaded = pd.read_csv('modified_data.csv')

# Calculate and print privacy metrics for reloaded modified data
k_anonymity_value = calculate_k_anonymity(modified_data_reloaded, modified_data_metrics['Quasi-Identifiers'])
l_diversity_value = calculate_l_diversity(modified_data_reloaded, modified_data_metrics['Quasi-Identifiers'], 'Diagnosis')
t_closeness_value = calculate_t_closeness(modified_data_reloaded, modified_data_metrics['Quasi-Identifiers'], 'Diagnosis')



# Log the final modified data and its metrics to W&B
modified_data_reloaded = pd.read_csv('modified_data.csv', dtype={'ZIP_code': str})

# Ensure that ZIP_code is explicitly converted to a string and handle any non-string values or NaNs
modified_data_reloaded['ZIP_code'] = modified_data_reloaded['ZIP_code'].astype(str).fillna('').str.zfill(3)
final_table = wandb.Table(dataframe=modified_data_reloaded)

wandb.log({"Modified Data": final_table})



# Print remeasured privacy metrics for verification
print("\nModified Data Details and Privacy Metrics after Reloading:")
for key, value in modified_data_metrics.items():
    print(f"{key}: {value}")
print(f"\nPrivacy metrics for Reloaded Modified Data:\nK-Anonymity: {k_anonymity_value}\nL-Diversity: {l_diversity_value}\nT-Closeness: {t_closeness_value:.4f}")

# End W&B run
wandb.finish()
