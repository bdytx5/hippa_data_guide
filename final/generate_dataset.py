# import pandas as pd
# import random

# # Define larger sets of possible values for the columns
# first_names = ['John', 'Jane', 'Emily', 'Michael', 'William', 'Sarah', 'Mark', 'Alex', 'Emma', 'Olivia',
#                'James', 'Sophia', 'Liam', 'Noah', 'Ava', 'Isabella', 'Mia', 'Charlotte', 'Amelia', 'Harper']
# last_names = ['Smith', 'Doe', 'Johnson', 'Davis', 'Brown', 'Wilson', 'Taylor', 'Clark', 'Lee', 'Walker',
#               'Martin', 'Allen', 'King', 'Wright', 'Scott', 'Green', 'Adams', 'Baker', 'Hall', 'Harris']
# street_names = ['Main St', 'Oak St', 'Pine Dr', 'Maple Ave', 'Elm St', 'Cedar Blvd', 'Birch Rd', 'Walnut Ln',
#                 'Chestnut St', 'Spruce St', 'Sycamore Rd', 'Willow Ave', 'Hickory Dr', 'Ash St', 'Poplar Ln']
# street_numbers = list(range(100, 1000))
# zip_codes = ['02138', '02139', '02140', '02141', '02142']
# birth_dates = pd.date_range('1940-01-01', '1990-12-31', periods=100).strftime('%Y-%m-%d').tolist()
# genders = ['Male', 'Female']
# diagnoses = ['Flu', 'Pneumonia', 'Asthma', 'Cancer', 'Heart Disease']
# procedures = ['Surgery', 'Physical Therapy', 'Chemotherapy', 'Radiology', 'Check-up']
# medications = ['Aspirin', 'Insulin', 'Antibiotics', 'Painkillers', 'Chemotherapy']
# party_affiliations = ['Democrat', 'Republican', 'Independent', 'Other']

# # Governor details for insertion
# governor = {
#     "Name": "William Weld",
#     "Address": "123 Main St",  # Unique address
#     "ZIP_code": '02138',
#     "Birth_date": '1945-07-31',
#     "Gender": 'Male',
#     "Party_affiliation": "Republican",
#     "Date_registered": '1980-01-01',
#     "Date_last_voted": '2024-01-01'
# }

# # Function to generate unique name and address
# def generate_unique_name(names_set):
#     while True:
#         name = f"{random.choice(first_names)} {random.choice(last_names)}"
#         if name not in names_set:
#             names_set.add(name)
#             return name

# def generate_unique_address(address_set):
#     while True:
#         address = f"{random.choice(street_numbers)} {random.choice(street_names)}"
#         if address not in address_set:
#             address_set.add(address)
#             return address

# # Create the voter dataset with 300 entries
# def generate_voter_data():
#     names_set = set()
#     addresses_set = set()

#     voter_data = {
#         "Name": [],
#         "Address": [],
#         "ZIP_code": [],
#         "Birth_date": [],
#         "Gender": [],
#         "Party_affiliation": [],
#         "Date_registered": [],
#         "Date_last_voted": []
#     }

#     for _ in range(299):  # 299 regular entries
#         voter_data["Name"].append(generate_unique_name(names_set))
#         voter_data["Address"].append(generate_unique_address(addresses_set))
#         voter_data["ZIP_code"].append(random.choice(zip_codes))
#         voter_data["Birth_date"].append(random.choice(birth_dates))
#         voter_data["Gender"].append(random.choice(genders))
#         voter_data["Party_affiliation"].append(random.choice(party_affiliations))
#         # Generate random registration and last voted dates
#         voter_data["Date_registered"].append(pd.to_datetime(random.choice(pd.date_range('2000-01-01', '2020-12-31'))).strftime('%Y-%m-%d'))
#         voter_data["Date_last_voted"].append(pd.to_datetime(random.choice(pd.date_range('2018-01-01', '2024-12-31'))).strftime('%Y-%m-%d'))

#     # Add the governor entry
#     voter_data["Name"].append(governor["Name"])
#     voter_data["Address"].append(governor["Address"])
#     voter_data["ZIP_code"].append(governor["ZIP_code"])
#     voter_data["Birth_date"].append(governor["Birth_date"])
#     voter_data["Gender"].append(governor["Gender"])
#     voter_data["Party_affiliation"].append(governor["Party_affiliation"])
#     voter_data["Date_registered"].append(governor["Date_registered"])
#     voter_data["Date_last_voted"].append(governor["Date_last_voted"])

#     return pd.DataFrame(voter_data)

# # Create the medical dataset with 100 entries
# def generate_medical_data():
#     medical_data = {
#         "ZIP_code": [],
#         "Birth_date": [],
#         "Gender": [],
#         "Diagnosis": [],
#         "Procedure": [],
#         "Medication": [],
#         "Total_charge": []
#     }

#     # For k-anonymity and l-diversity illustration
#     # First 10 entries: Same quasi-identifiers, same diagnosis (low l-diversity)
#     for _ in range(10):
#         medical_data["ZIP_code"].append('02138')
#         medical_data["Birth_date"].append('1980-06-15')  # Fixed birth date
#         medical_data["Gender"].append('Female')
#         medical_data["Diagnosis"].append('Cancer')  # Same diagnosis
#         medical_data["Procedure"].append(random.choice(procedures))
#         medical_data["Medication"].append(random.choice(medications))
#         medical_data["Total_charge"].append(round(random.uniform(1000, 10000), 2))

#     # Next 10 entries: Same quasi-identifiers, diverse diagnoses (improved l-diversity)
#     for _ in range(10):
#         medical_data["ZIP_code"].append('02138')
#         medical_data["Birth_date"].append('1980-06-15')  # Fixed birth date
#         medical_data["Gender"].append('Female')
#         medical_data["Diagnosis"].append(random.choice(['Flu', 'Pneumonia', 'Asthma']))
#         medical_data["Procedure"].append(random.choice(procedures))
#         medical_data["Medication"].append(random.choice(medications))
#         medical_data["Total_charge"].append(round(random.uniform(1000, 10000), 2))

#     # For t-closeness illustration
#     # Next 10 entries: Same quasi-identifiers, skewed diagnosis distribution
#     for _ in range(10):
#         medical_data["ZIP_code"].append('02139')
#         medical_data["Birth_date"].append('1975-08-20')  # Fixed birth date
#         medical_data["Gender"].append('Male')
#         medical_data["Diagnosis"].append('Heart Disease')  # Overrepresented diagnosis
#         medical_data["Procedure"].append(random.choice(procedures))
#         medical_data["Medication"].append(random.choice(medications))
#         medical_data["Total_charge"].append(round(random.uniform(1000, 10000), 2))

#     # Remaining entries: Random data
#     for _ in range(70):
#         medical_data["ZIP_code"].append(random.choice(zip_codes))
#         medical_data["Birth_date"].append(random.choice(birth_dates))
#         medical_data["Gender"].append(random.choice(genders))
#         medical_data["Diagnosis"].append(random.choice(diagnoses))
#         medical_data["Procedure"].append(random.choice(procedures))
#         medical_data["Medication"].append(random.choice(medications))
#         medical_data["Total_charge"].append(round(random.uniform(100, 10000), 2))

#     # Add the governor's medical record
#     medical_data["ZIP_code"][0] = governor["ZIP_code"]
#     medical_data["Birth_date"][0] = governor["Birth_date"]
#     medical_data["Gender"][0] = governor["Gender"]
#     medical_data["Diagnosis"][0] = "Heart Disease"
#     medical_data["Procedure"][0] = "Surgery"
#     medical_data["Medication"][0] = "Aspirin"
#     medical_data["Total_charge"][0] = 8000.00

#     return pd.DataFrame(medical_data)

# # Generate and save the datasets
# voter_df = generate_voter_data()
# medical_df = generate_medical_data()

# # Ensure ZIP code columns are stored as 5-digit strings
# voter_df['ZIP_code'] = voter_df['ZIP_code'].apply(lambda x: f"{int(x):05d}")
# medical_df['ZIP_code'] = medical_df['ZIP_code'].apply(lambda x: f"{int(x):05d}")

# # Save to CSV files
# voter_df.to_csv('synthetic_voter_data_with_governor.csv', index=False)
# medical_df.to_csv('synthetic_medical_data_with_governor.csv', index=False)

# print("CSV files generated successfully!")


import pandas as pd
import random
import wandb

# Initialize a new W&B run
wandb.init(project="synthetic_data_de-identification")

# Define larger sets of possible values for the columns
first_names = ['John', 'Jane', 'Emily', 'Michael', 'William', 'Sarah', 'Mark', 'Alex', 'Emma', 'Olivia',
               'James', 'Sophia', 'Liam', 'Noah', 'Ava', 'Isabella', 'Mia', 'Charlotte', 'Amelia', 'Harper']
last_names = ['Smith', 'Doe', 'Johnson', 'Davis', 'Brown', 'Wilson', 'Taylor', 'Clark', 'Lee', 'Walker',
              'Martin', 'Allen', 'King', 'Wright', 'Scott', 'Green', 'Adams', 'Baker', 'Hall', 'Harris']
street_names = ['Main St', 'Oak St', 'Pine Dr', 'Maple Ave', 'Elm St', 'Cedar Blvd', 'Birch Rd', 'Walnut Ln',
                'Chestnut St', 'Spruce St', 'Sycamore Rd', 'Willow Ave', 'Hickory Dr', 'Ash St', 'Poplar Ln']
street_numbers = list(range(100, 1000))
zip_codes = ['02138', '02139', '02140', '02141', '02142']
birth_dates = pd.date_range('1940-01-01', '1990-12-31', periods=100).strftime('%Y-%m-%d').tolist()
genders = ['Male', 'Female']
diagnoses = ['Flu', 'Pneumonia', 'Asthma', 'Cancer', 'Heart Disease']
procedures = ['Surgery', 'Physical Therapy', 'Chemotherapy', 'Radiology', 'Check-up']
medications = ['Aspirin', 'Insulin', 'Antibiotics', 'Painkillers', 'Chemotherapy']
party_affiliations = ['Democrat', 'Republican', 'Independent', 'Other']

# Governor details for insertion
governor = {
    "Name": "William Weld",
    "Address": "123 Main St",  # Unique address
    "ZIP_code": '02138',
    "Birth_date": '1945-07-31',
    "Gender": 'Male',
    "Party_affiliation": "Republican",
    "Date_registered": '1980-01-01',
    "Date_last_voted": '2024-01-01'
}

# Function to generate unique name and address
def generate_unique_name(names_set):
    while True:
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        if name not in names_set:
            names_set.add(name)
            return name

def generate_unique_address(address_set):
    while True:
        address = f"{random.choice(street_numbers)} {random.choice(street_names)}"
        if address not in address_set:
            address_set.add(address)
            return address

# Create the voter dataset with 300 entries
def generate_voter_data():
    names_set = set()
    addresses_set = set()

    voter_data = {
        "Name": [],
        "Address": [],
        "ZIP_code": [],
        "Birth_date": [],
        "Gender": [],
        "Party_affiliation": [],
        "Date_registered": [],
        "Date_last_voted": []
    }

    for _ in range(299):  # 299 regular entries
        voter_data["Name"].append(generate_unique_name(names_set))
        voter_data["Address"].append(generate_unique_address(addresses_set))
        voter_data["ZIP_code"].append(random.choice(zip_codes))
        voter_data["Birth_date"].append(random.choice(birth_dates))
        voter_data["Gender"].append(random.choice(genders))
        voter_data["Party_affiliation"].append(random.choice(party_affiliations))
        # Generate random registration and last voted dates
        voter_data["Date_registered"].append(pd.to_datetime(random.choice(pd.date_range('2000-01-01', '2020-12-31'))).strftime('%Y-%m-%d'))
        voter_data["Date_last_voted"].append(pd.to_datetime(random.choice(pd.date_range('2018-01-01', '2024-12-31'))).strftime('%Y-%m-%d'))

    # Add the governor entry
    voter_data["Name"].append(governor["Name"])
    voter_data["Address"].append(governor["Address"])
    voter_data["ZIP_code"].append(governor["ZIP_code"])
    voter_data["Birth_date"].append(governor["Birth_date"])
    voter_data["Gender"].append(governor["Gender"])
    voter_data["Party_affiliation"].append(governor["Party_affiliation"])
    voter_data["Date_registered"].append(governor["Date_registered"])
    voter_data["Date_last_voted"].append(governor["Date_last_voted"])

    return pd.DataFrame(voter_data)

# Create the medical dataset with 100 entries
def generate_medical_data():
    medical_data = {
        "ZIP_code": [],
        "Birth_date": [],
        "Gender": [],
        "Diagnosis": [],
        "Procedure": [],
        "Medication": [],
        "Total_charge": []
    }

    # For k-anonymity and l-diversity illustration
    # First 10 entries: Same quasi-identifiers, same diagnosis (low l-diversity)
    for _ in range(10):
        medical_data["ZIP_code"].append('02138')
        medical_data["Birth_date"].append('1980-06-15')  # Fixed birth date
        medical_data["Gender"].append('Female')
        medical_data["Diagnosis"].append('Cancer')  # Same diagnosis
        medical_data["Procedure"].append(random.choice(procedures))
        medical_data["Medication"].append(random.choice(medications))
        medical_data["Total_charge"].append(round(random.uniform(1000, 10000), 2))

    # Next 10 entries: Same quasi-identifiers, diverse diagnoses (improved l-diversity)
    for _ in range(10):
        medical_data["ZIP_code"].append('02138')
        medical_data["Birth_date"].append('1980-06-15')  # Fixed birth date
        medical_data["Gender"].append('Female')
        medical_data["Diagnosis"].append(random.choice(['Flu', 'Pneumonia', 'Asthma']))
        medical_data["Procedure"].append(random.choice(procedures))
        medical_data["Medication"].append(random.choice(medications))
        medical_data["Total_charge"].append(round(random.uniform(1000, 10000), 2))

    # For t-closeness illustration
    # Next 10 entries: Same quasi-identifiers, skewed diagnosis distribution
    for _ in range(10):
        medical_data["ZIP_code"].append('02139')
        medical_data["Birth_date"].append('1975-08-20')  # Fixed birth date
        medical_data["Gender"].append('Male')
        medical_data["Diagnosis"].append('Heart Disease')  # Overrepresented diagnosis
        medical_data["Procedure"].append(random.choice(procedures))
        medical_data["Medication"].append(random.choice(medications))
        medical_data["Total_charge"].append(round(random.uniform(1000, 10000), 2))

    # Remaining entries: Random data
    for _ in range(70):
        medical_data["ZIP_code"].append(random.choice(zip_codes))
        medical_data["Birth_date"].append(random.choice(birth_dates))
        medical_data["Gender"].append(random.choice(genders))
        medical_data["Diagnosis"].append(random.choice(diagnoses))
        medical_data["Procedure"].append(random.choice(procedures))
        medical_data["Medication"].append(random.choice(medications))
        medical_data["Total_charge"].append(round(random.uniform(100, 10000), 2))

    # Add the governor's medical record
    medical_data["ZIP_code"][0] = governor["ZIP_code"]
    medical_data["Birth_date"][0] = governor["Birth_date"]
    medical_data["Gender"][0] = governor["Gender"]
    medical_data["Diagnosis"][0] = "Heart Disease"
    medical_data["Procedure"][0] = "Surgery"
    medical_data["Medication"][0] = "Aspirin"
    medical_data["Total_charge"][0] = 8000.00

    return pd.DataFrame(medical_data)

# Generate and save the datasets
voter_df = generate_voter_data()
medical_df = generate_medical_data()

# Ensure ZIP code columns are stored as 5-digit strings
voter_df['ZIP_code'] = voter_df['ZIP_code'].apply(lambda x: f"{int(x):05d}")
medical_df['ZIP_code'] = medical_df['ZIP_code'].apply(lambda x: f"{int(x):05d}")

# Log the voter dataset as a W&B Table
voter_table = wandb.Table(dataframe=voter_df)
wandb.log({"Voter Dataset": voter_table})

# Log the medical dataset as a W&B Table
medical_table = wandb.Table(dataframe=medical_df)
wandb.log({"Medical Dataset": medical_table})

# Save the datasets to CSV files
voter_df.to_csv('synthetic_voter_data_with_governor.csv', index=False)
medical_df.to_csv('synthetic_medical_data_with_governor.csv', index=False)

print("CSV files and W&B tables generated successfully!")
