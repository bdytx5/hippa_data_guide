
import pandas as pd
import numpy as np

# Load both the voter and medical datasets, specifying data types
dtype_spec = {
    'ZIP_code': str,
    'Birth_date': str,
    'Gender': str
}

voter_data = pd.read_csv('synthetic_voter_data_with_governor.csv', dtype=dtype_spec)
medical_data = pd.read_csv('synthetic_medical_data_with_governor.csv', dtype=dtype_spec)

# Define the cross-reference points based on the "Governor-like" entry
governor_zip = '02138'
governor_birth_date = '1945-07-31'
governor_gender = 'Male'

# Function to calculate k-anonymity
def calculate_k_anonymity(data, quasi_identifiers):
    grouped = data.groupby(quasi_identifiers)
    group_sizes = grouped.size()
    k_anonymity = group_sizes.min()
    print(f"\nK-Anonymity: {k_anonymity}")
    return group_sizes

# Function to calculate l-diversity
def calculate_l_diversity(data, quasi_identifiers, sensitive_attribute):
    grouped = data.groupby(quasi_identifiers)
    l_diversity = grouped[sensitive_attribute].nunique().min()
    print(f"\nL-Diversity: {l_diversity}")
    return grouped[sensitive_attribute].nunique()

# Function to calculate t-closeness
def calculate_t_closeness(data, quasi_identifiers, sensitive_attribute):
    overall_distribution = data[sensitive_attribute].value_counts(normalize=True)
    grouped = data.groupby(quasi_identifiers)
    max_t = 0
    for name, group in grouped:
        group_distribution = group[sensitive_attribute].value_counts(normalize=True)
        t_distance = abs(overall_distribution - group_distribution).sum() / 2
        max_t = max(max_t, t_distance)
    print(f"\nT-Closeness: {max_t}")
    return max_t

# Define quasi-identifiers and sensitive attribute
quasi_identifiers = ['ZIP_code', 'Birth_date', 'Gender']
sensitive_attribute = 'Diagnosis'

# Calculate k-anonymity
group_sizes = calculate_k_anonymity(medical_data, quasi_identifiers)

# Calculate l-diversity
l_diversity = calculate_l_diversity(medical_data, quasi_identifiers, sensitive_attribute)

# Calculate t-closeness
t_closeness = calculate_t_closeness(medical_data, quasi_identifiers, sensitive_attribute)

# Print group sizes and l-diversity for each group
print("\nGroup sizes and L-Diversity per group:")
group_info = pd.DataFrame({
    'Group Size': group_sizes,
    'L-Diversity': l_diversity
})
print(group_info)


# Perform the cross-reference on the voter data
matched_voter = voter_data[
    (voter_data['ZIP_code'] == governor_zip) &
    (voter_data['Birth_date'] == governor_birth_date) &
    (voter_data['Gender'] == governor_gender)
]

# Perform the cross-reference on the medical data
matched_medical = medical_data[
    (medical_data['ZIP_code'] == governor_zip) &
    (medical_data['Birth_date'] == governor_birth_date) &
    (medical_data['Gender'] == governor_gender)
]

# Check that exactly one record is found in both datasets
if len(matched_voter) == 1 and len(matched_medical) == 1:
    print("\nCross-reference successful: This individual appears in both datasets!")
    print("Matched Voter Record:")
    print(matched_voter)
    print("\nMatched Medical Record:")
    print(matched_medical)
else:
    print("\nCross-reference failed: No unique match found in both datasets.")
    if len(matched_voter) > 1:
        print(f"Warning: Multiple voter records found ({len(matched_voter)})")
    if len(matched_medical) > 1:
        print(f"Warning: Multiple medical records found ({len(matched_medical)})")
