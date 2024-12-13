import json
from collections import Counter
from datetime import datetime
import numpy as np

# Load the JSON data
with open('DataEngineeringQ2.json', 'r') as file:
    data = json.load(file)

def calculate_age(birth_date):
    if not birth_date:
        return None
    birth_date = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_age_group(age):
    if age is None:
        return None
    if age <= 12:
        return "Child"
    elif age <= 19:
        return "Teen"
    elif age <= 59:
        return "Adult"
    else:
        return "Senior"

def is_valid_mobile(phone_number):
    if phone_number.startswith("+91"):
        phone_number = phone_number[3:]
    elif phone_number.startswith("91"):
        phone_number = phone_number[2:]
    if len(phone_number) == 10 and phone_number.isdigit():
        num = int(phone_number)
        if 6000000000 <= num <= 9999999999:
            return True
    return False

# Q1: Missing values percentage
total_records = len(data)
missing_counts = {"firstName": 0, "lastName": 0, "birthDate": 0}
for record in data:
    patient = record.get("patientDetails", {})
    if not patient.get("firstName"):
        missing_counts["firstName"] += 1
    if not patient.get("lastName"):
        missing_counts["lastName"] += 1
    if not patient.get("birthDate"):
        missing_counts["birthDate"] += 1
missing_percentages = {col: (count / total_records) * 100 for col, count in missing_counts.items()}

# Q2: Female percentage after imputation
gender_counts = Counter(record.get("patientDetails", {}).get("gender", "") for record in data)
mode_gender = gender_counts.most_common(1)[0][0]
imputed_female_count = sum(
    1 for record in data if record.get("patientDetails", {}).get("gender", mode_gender) == "F"
)
female_percentage = (imputed_female_count / total_records) * 100

# Q3: Count of Adults in ageGroup
age_groups = {"Child": 0, "Teen": 0, "Adult": 0, "Senior": 0}
for record in data:
    birth_date = record.get("patientDetails", {}).get("birthDate")
    age = calculate_age(birth_date)
    age_group = get_age_group(age)
    if age_group:
        age_groups[age_group] += 1
adult_count = age_groups["Adult"]

# Q4: Average number of medicines prescribed
total_medicines = 0
for record in data:
    medicines = record.get("consultationData", {}).get("medicines", [])
    total_medicines += len(medicines)
average_medicines = total_medicines / total_records

# Q5: 3rd most frequently prescribed medicine name
medicine_counter = Counter(
    med["medicineName"]
    for record in data
    for med in record.get("consultationData", {}).get("medicines", [])
)
third_most_frequent_medicine = medicine_counter.most_common(3)[-1][0]

# Q6: Active/Inactive medicines percentage
active_count = 0
inactive_count = 0
for record in data:
    for med in record.get("consultationData", {}).get("medicines", []):
        if med["isActive"]:
            active_count += 1
        else:
            inactive_count += 1
total_medicines = active_count + inactive_count
active_percentage = (active_count / total_medicines) * 100 if total_medicines else 0
inactive_percentage = (inactive_count / total_medicines) * 100 if total_medicines else 0

# Q10: Count of valid mobile numbers
valid_mobile_count = 0
for record in data:
    phone_number = record.get("phoneNumber", "")
    if is_valid_mobile(phone_number):
        valid_mobile_count += 1

# Q11: Pearson correlation
ages = []
medicine_counts = []
for record in data:
    birth_date = record.get("patientDetails", {}).get("birthDate")
    age = calculate_age(birth_date)
    medicines = record.get("consultationData", {}).get("medicines", [])
    if age is not None:
        ages.append(age)
        medicine_counts.append(len(medicines))
if len(ages) > 1 and len(medicine_counts) > 1:
    correlation = np.corrcoef(ages, medicine_counts)[0, 1]
else:
    correlation = 0

# Results
results = {
    "missing_percentages": {k: round(v, 2) for k, v in missing_percentages.items()},
    "female_percentage": round(female_percentage, 2),
    "adult_count": adult_count,
    "average_medicines": round(average_medicines, 2),
    "third_most_frequent_medicine": third_most_frequent_medicine,
    "medicine_distribution": (round(active_percentage, 2), round(inactive_percentage, 2)),
    "valid_mobile_count": valid_mobile_count,
    "pearson_correlation": round(correlation, 2)
}

print(results)
