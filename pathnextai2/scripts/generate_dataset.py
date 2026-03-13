"""
generate_dataset.py
-------------------
Generates a synthetic dataset of 3000 student profiles
for training the career recommendation ML model.

Each row represents one student with:
- Stream (Science PCM / Science PCB / Commerce / Arts)
- Subject marks (0-100)
- Interest flags (binary 0 or 1)
- Soft skill ratings (1-5)
- Career label (target)

Key rule enforced:
- PCM students → biology = 0
- PCB students → maths = 0

Run this file once:
    python generate_dataset.py
"""

import pandas as pd
import numpy as np
import random
import os

# So results are the same every time we run
random.seed(42)
np.random.seed(42)

# ------------------------------------------------------------------
# All possible careers we predict
# ------------------------------------------------------------------
CAREERS = [
    "Software Engineer",
    "Data Scientist",
    "Cybersecurity Analyst",
    "Doctor",
    "Biotechnologist",
    "Chartered Accountant",
    "Investment Banker",
    "Entrepreneur",
    "Lawyer",
    "Journalist",
    "UX Designer",
    "Psychologist",
    "Architect",
    "Digital Marketer",
    "Teacher",
]

# ------------------------------------------------------------------
# All interest columns in our dataset
# ------------------------------------------------------------------
INTEREST_COLS = [
    "interest_tech",
    "interest_ai",
    "interest_design",
    "interest_finance",
    "interest_law",
    "interest_medicine",
    "interest_psychology",
    "interest_writing",
    "interest_public_speaking",
    "interest_creativity",
    "interest_marketing",
    "interest_entrepreneurship",
    "interest_biology",
    "interest_data",
    "interest_cybersecurity",
    "interest_architecture",
    "interest_teaching",
    "interest_social_work",
    "interest_economics",
    "interest_politics",
    "interest_journalism",
    "interest_gaming",
    "interest_music",
    "interest_film",
    "interest_photography",
    "interest_environment",
    "interest_astronomy",
    "interest_animation",
    "interest_sports",
    "interest_healthcare",
]

# ------------------------------------------------------------------
# Soft skill columns
# ------------------------------------------------------------------
SKILL_COLS = [
    "communication",
    "leadership",
    "creativity",
    "analytical_thinking",
    "problem_solving",
    "teamwork",
    "empathy",
    "critical_thinking",
    "time_management",
    "adaptability",
]

# ------------------------------------------------------------------
# Rules: what subjects, interests, skills match each career
# ------------------------------------------------------------------
CAREER_RULES = {
    "Software Engineer": {
        "streams": ["Science PCM"],
        "high_marks": {"maths": (75, 100), "physics": (65, 95)},
        "key_interests": ["interest_tech", "interest_ai", "interest_gaming", "interest_data"],
        "key_skills": ["analytical_thinking", "problem_solving", "critical_thinking"],
    },
    "Data Scientist": {
        "streams": ["Science PCM"],
        "high_marks": {"maths": (80, 100), "physics": (65, 90)},
        "key_interests": ["interest_ai", "interest_data", "interest_tech", "interest_economics"],
        "key_skills": ["analytical_thinking", "critical_thinking", "problem_solving"],
    },
    "Cybersecurity Analyst": {
        "streams": ["Science PCM"],
        "high_marks": {"maths": (70, 95), "physics": (60, 90)},
        "key_interests": ["interest_cybersecurity", "interest_tech", "interest_gaming"],
        "key_skills": ["analytical_thinking", "problem_solving", "critical_thinking"],
    },
    "Doctor": {
        "streams": ["Science PCB"],
        "high_marks": {"biology": (80, 100), "chemistry": (75, 100)},
        "key_interests": ["interest_medicine", "interest_healthcare", "interest_biology"],
        "key_skills": ["empathy", "critical_thinking", "problem_solving", "time_management"],
    },
    "Biotechnologist": {
        "streams": ["Science PCB"],
        "high_marks": {"biology": (75, 100), "chemistry": (70, 95)},
        "key_interests": ["interest_biology", "interest_medicine", "interest_environment"],
        "key_skills": ["analytical_thinking", "problem_solving", "critical_thinking"],
    },
    "Chartered Accountant": {
        "streams": ["Commerce"],
        "high_marks": {"accounts": (80, 100), "maths": (70, 95), "economics": (65, 90)},
        "key_interests": ["interest_finance", "interest_economics", "interest_entrepreneurship"],
        "key_skills": ["analytical_thinking", "time_management", "critical_thinking"],
    },
    "Investment Banker": {
        "streams": ["Commerce"],
        "high_marks": {"economics": (75, 100), "maths": (70, 95), "accounts": (65, 90)},
        "key_interests": ["interest_finance", "interest_economics", "interest_entrepreneurship"],
        "key_skills": ["analytical_thinking", "leadership", "communication"],
    },
    "Entrepreneur": {
        "streams": ["Commerce"],
        "high_marks": {"business": (75, 100), "economics": (65, 90)},
        "key_interests": ["interest_entrepreneurship", "interest_marketing", "interest_creativity"],
        "key_skills": ["leadership", "creativity", "adaptability", "communication"],
    },
    "Lawyer": {
        "streams": ["Arts"],
        "high_marks": {"political_science": (75, 100), "history": (65, 95)},
        "key_interests": ["interest_law", "interest_public_speaking", "interest_politics"],
        "key_skills": ["communication", "critical_thinking", "analytical_thinking"],
    },
    "Journalist": {
        "streams": ["Arts"],
        "high_marks": {"history": (65, 90), "political_science": (60, 90)},
        "key_interests": ["interest_journalism", "interest_writing", "interest_public_speaking"],
        "key_skills": ["communication", "creativity", "adaptability"],
    },
    "UX Designer": {
        "streams": ["Arts", "Commerce"],
        "high_marks": {"psychology": (65, 90)},
        "key_interests": ["interest_design", "interest_creativity", "interest_tech", "interest_animation"],
        "key_skills": ["creativity", "empathy", "communication", "analytical_thinking"],
    },
    "Psychologist": {
        "streams": ["Arts"],
        "high_marks": {"psychology": (75, 100), "sociology": (65, 90)},
        "key_interests": ["interest_psychology", "interest_social_work", "interest_teaching"],
        "key_skills": ["empathy", "communication", "critical_thinking"],
    },
    "Architect": {
        "streams": ["Science PCM"],
        "high_marks": {"maths": (70, 95), "physics": (65, 90)},
        "key_interests": ["interest_architecture", "interest_design", "interest_creativity"],
        "key_skills": ["creativity", "analytical_thinking", "problem_solving"],
    },
    "Digital Marketer": {
        "streams": ["Commerce", "Arts"],
        "high_marks": {"business": (65, 90), "economics": (60, 85)},
        "key_interests": ["interest_marketing", "interest_creativity", "interest_writing", "interest_film"],
        "key_skills": ["creativity", "communication", "adaptability"],
    },
    "Teacher": {
        "streams": ["Arts"],
        "high_marks": {"history": (65, 90), "sociology": (60, 85)},
        "key_interests": ["interest_teaching", "interest_social_work", "interest_psychology"],
        "key_skills": ["communication", "empathy", "leadership"],
    },
}

# All subject columns in our dataset
ALL_SUBJECT_COLS = [
    "physics", "chemistry", "maths", "biology",
    "accounts", "business", "economics",
    "history", "political_science", "geography",
    "psychology", "sociology", "english"
]

# Which subjects belong to which stream
STREAM_SUBJECTS = {
    "Science PCM": ["physics", "chemistry", "maths", "english"],
    "Science PCB": ["physics", "chemistry", "biology", "english"],
    "Commerce":    ["accounts", "business", "economics", "maths", "english"],
    "Arts":        ["history", "political_science", "geography", "psychology", "sociology", "english"],
}


def generate_one_student(career_label):
    """
    Create one student profile that logically fits the given career.
    Returns a dict with all columns.
    """
    rule = CAREER_RULES[career_label]

    # Pick a stream from the allowed streams for this career
    stream = random.choice(rule["streams"])

    # --- Build marks ---
    # Start with zero for all subjects
    marks = {subj: 0 for subj in ALL_SUBJECT_COLS}

    # Give realistic marks for stream subjects
    for subj in STREAM_SUBJECTS[stream]:
        marks[subj] = random.randint(50, 85)

    # Give higher marks for key subjects of this career
    for subj, (low, high) in rule["high_marks"].items():
        if subj in STREAM_SUBJECTS[stream]:  # only if this subject is in their stream
            marks[subj] = random.randint(low, high)

    # PCM rule: biology must be 0
    if stream == "Science PCM":
        marks["biology"] = 0

    # PCB rule: maths must be 0
    if stream == "Science PCB":
        marks["maths"] = 0

    # Add small random noise
    for subj in STREAM_SUBJECTS[stream]:
        noise = random.randint(-8, 8)
        marks[subj] = max(0, min(100, marks[subj] + noise))

    # --- Build interests ---
    # Start with all zeros
    interests = {col: 0 for col in INTEREST_COLS}

    # Turn on key interests for this career
    for col in rule["key_interests"]:
        interests[col] = 1

    # Randomly turn on 2-4 more interests
    other_interests = [c for c in INTEREST_COLS if c not in rule["key_interests"]]
    random_extra = random.sample(other_interests, k=random.randint(2, 4))
    for col in random_extra:
        interests[col] = 1

    # --- Build soft skills ---
    skills = {}
    for skill in SKILL_COLS:
        if skill in rule["key_skills"]:
            # High score for key skills
            skills[skill] = random.randint(3, 5)
        else:
            # Random score for other skills
            skills[skill] = random.randint(1, 5)

    # --- Combine everything ---
    row = {"stream": stream, "career": career_label}
    row.update(marks)
    row.update(interests)
    row.update(skills)

    return row


def generate_dataset(n_rows=3000):
    """
    Generate n_rows student profiles spread across all careers.
    """
    print(f"Generating {n_rows} student profiles...")

    rows = []
    rows_per_career = n_rows // len(CAREERS)

    for career in CAREERS:
        for _ in range(rows_per_career):
            rows.append(generate_one_student(career))

    # Fill remaining rows
    remaining = n_rows - len(rows)
    for i in range(remaining):
        rows.append(generate_one_student(CAREERS[i % len(CAREERS)]))

    # Shuffle so careers aren't all grouped together
    random.shuffle(rows)

    df = pd.DataFrame(rows)

    print(f"Dataset shape: {df.shape}")
    print(f"\nCareer distribution:")
    print(df["career"].value_counts())
    print(f"\nStream distribution:")
    print(df["stream"].value_counts())

    return df


if __name__ == "__main__":
    df = generate_dataset(3000)

    # Save to dataset folder
    os.makedirs("../dataset", exist_ok=True)
    output_path = "../dataset/career_dataset.csv"
    df.to_csv(output_path, index=False)
    print(f"\nDataset saved to: {output_path}")
