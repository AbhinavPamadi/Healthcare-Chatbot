import pandas as pd
import csv

# -----------------------------
# Load Training Data
# -----------------------------

training = pd.read_csv("Data/Training.csv")

symptoms = list(training.columns[:-1])

disease_rules = {}

for _, row in training.iterrows():
    disease = row["prognosis"]
    sym_list = [symptoms[i] for i in range(len(symptoms)) if row.iloc[i] == 1]
    disease_rules[disease] = sym_list


# -----------------------------
# Dictionaries
# -----------------------------

severityDictionary = {}
description_list = {}
precautionDictionary = {}

# -----------------------------
# Symptom alias mapping
# -----------------------------

symptom_alias = {
    "cold": ["runny_nose", "continuous_sneezing", "chills"],
    "fever": ["high_fever"],
    "cough": ["cough"],
    "headache": ["headache"],
    "vomiting": ["vomiting"],
    "stomach pain": ["abdominal_pain"],
    "sore throat": ["throat_irritation"]
}

# -----------------------------
# Load CSV metadata
# -----------------------------

def load_severity():

    with open("MasterData/symptom_severity.csv") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 2:
                continue

            severityDictionary[row[0]] = int(row[1])


def load_description():

    with open("MasterData/symptom_Description.csv") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 2:
                continue

            description_list[row[0]] = row[1]


def load_precautions():

    with open("MasterData/symptom_precaution.csv") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 5:
                continue

            precautionDictionary[row[0]] = [row[1], row[2], row[3], row[4]]


# -----------------------------
# Symptom suggestion
# -----------------------------

def suggest_symptoms(word):

    matches = []

    for s in symptoms:

        if word in s or s in word:
            matches.append(s)

    return matches


# -----------------------------
# Match symptom
# -----------------------------

def match_symptom(user_input):

    user_input = user_input.lower()

    if user_input in symptom_alias:
        return symptom_alias[user_input]

    user_input = user_input.replace(" ", "_")

    matches = suggest_symptoms(user_input)

    return matches


# -----------------------------
# Rule scoring
# -----------------------------

def disease_score(user_symptoms):

    scores = {}

    for disease, rule_symptoms in disease_rules.items():

        matched = list(set(user_symptoms) & set(rule_symptoms))

        if len(matched) < 2:
            continue

        matched_severity = sum(severityDictionary.get(s, 1) for s in matched)

        max_severity = sum(severityDictionary.get(s, 1) for s in rule_symptoms)

        score = matched_severity / max_severity

        scores[disease] = score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return ranked


# -----------------------------
# Severity check
# -----------------------------

def check_severity(user_symptoms, days):

    total = 0

    for s in user_symptoms:
        total += severityDictionary.get(s, 0)

    score = (total * days) / (len(user_symptoms) + 1)

    if score > 15:
        print("\n⚠ You should consult a doctor.")
    else:
        print("\n✓ Symptoms appear mild but take precautions.")


# -----------------------------
# Chatbot
# -----------------------------

def chatbot():

    print("\n------------- Healthcare Chatbot -------------")

    name = input("Enter your name: ")
    print("Hello", name)

    user_symptoms = []

    while True:

        inp = input("\nEnter symptom (or 'done'): ")

        if inp.lower() == "done":
            break

        matches = match_symptom(inp)

        if len(matches) == 0:
            print("Symptom not found. Try again.")
            continue

        if len(matches) > 1:

            print("Did you mean:")

            for i, m in enumerate(matches):
                print(i, m)

            choice = int(input("Select: "))
            symptom = matches[choice]

        else:
            symptom = matches[0]

        user_symptoms.append(symptom)

    if len(user_symptoms) == 0:
        print("\nNo symptoms entered.")
        return

    days = int(input("\nFrom how many days? "))

    check_severity(user_symptoms, days)

    ranked = disease_score(user_symptoms)

    if len(ranked) == 0:
        print("\nNot enough symptoms to determine disease.")
        print("Please provide more symptoms.")
        return

    print("\nPossible diseases:\n")

    for disease, score in ranked[:3]:

        print("Disease:", disease)
        print("Match Score:", round(score * 100, 2), "%")

        if disease in description_list:
            print("Description:", description_list[disease])

        if disease in precautionDictionary:

            print("Precautions:")

            for p in precautionDictionary[disease]:
                print("-", p)

        print()


# -----------------------------
# Run
# -----------------------------

load_severity()
load_description()
load_precautions()

chatbot()