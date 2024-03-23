import numpy as np


def preprocess(input):
    # Filter out the entry with label 'neutral'
    filtered_data = [item for item in input[0] if item['label'] != 'neutral']

    # Sort the filtered data alphabetically by the 'label' field
    sorted_data = sorted(filtered_data, key=lambda x: x['label'])

    # Extract just the values (scores)
    values = [item['score'] for item in sorted_data]

    N = len(values)

    # Takes an input of 6 emotions and turns it into 21
    for i in range(N):
        for j in range(i + 1, N):
            values.append(0.5 * (values[i] + values[j]))

    # Calculate the magnitude of the vector
    magnitude = np.linalg.norm(values)

    # Check if the magnitude is not zero to avoid division by zero
    if magnitude != 0:
        # Normalize the vector by dividing each element by the magnitude
        normalized_vector = values / magnitude
    else:
        # If the magnitude is zero, return the original vector (to avoid division by zero)
        normalized_vector = values

    return normalized_vector

labels = [
    "Anger",
    "Disgust",
    "Fear",
    "Joy",
    "Sadness",
    "Surprise",
    "Hatred",
    "Terror",
    "Rage",
    "Bitterness",
    "Fury",
    "Horrified",
    "Confusion",
    "Despise",
    "Revulsion",
    "Diabolical",
    "Sorrow",
    "Shock",
    "Ambivalence",
    "Elation",
    "Grief"
]

def print_with_labels(input):
    map = {}
    for i in range(len(input)):
        map[labels[i]] = input[i]

    # Sort the dictionary by values
    sorted_mapping = sorted(map.items(), key=lambda x: -x[1])

    # Print the labels and values sorted by values
    for label, value in sorted_mapping:
        print(f"{label}: {value}")
        

if __name__ == "__main__":
    data = [[{'label': 'neutral', 'score': 0.29118889570236206},
             {'label': 'fear', 'score': 0.2906285226345062},
             {'label': 'anger', 'score': 0.1463823765516281},
             {'label': 'sadness', 'score': 0.14210467040538788},
             {'label': 'disgust', 'score': 0.07558312267065048},
             {'label': 'surprise', 'score': 0.030138494446873665},
             {'label': 'joy', 'score': 0.023973964154720306}]]

    print_with_labels(preprocess(data))
