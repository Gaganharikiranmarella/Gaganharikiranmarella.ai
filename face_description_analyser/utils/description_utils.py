def build_description(gender, age, emotion, head_pose):
    parts = []

    if gender != "Unknown":
        parts.append(f"A {gender.lower()}")
    else:
        parts.append("A person")

    if age != "Unknown":
        parts.append(f"around age {age.replace('(', '').replace(')', '')}")

    if emotion != "Unknown":
        parts.append(f"appears {emotion.lower()}")

    if head_pose != "Unknown":
        parts.append(f"with head {head_pose.lower()}")

    return " ".join(parts) + "."
