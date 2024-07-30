import numpy as np
import pandas as pd

# Scores from the judges
scores = {
    'Room_A': {
        'Judge_1': [7, 9, 8, 9, 10],
        'Judge_2': [7, 7, 8, 5, 5],
        'Judge_3': [4, 7, 8, 6, 6]
    },
    'Room_B': {
        'Judge_4': [3, 2, 6, 6, 5],
        'Judge_5': [4, 7, 9, 8, 7],
        'Judge_6': [6, 6, 8, 9, 9]
    }
}

def calculate_final_scores(scores):
    final_scores = {}
    for room, judges in scores.items():
        room_scores = []
        for judges, team_scores in judges.items():
            room_scores.append(team_scores)
        final_scores[room] = np.round(np.mean(room_scores, axis=0), decimals=2)
    return final_scores

print("Unsorted Final Scores:")
print(calculate_final_scores(scores))

def order_scores_with_teams(final_scores, team_names):
    ordered_scores = {}
    for room, scores in final_scores.items():
        team_scores = list(zip(team_names[room], scores))
        sorted_team_scores = sorted(team_scores, key=lambda x: x[1])
        ordered_scores[room] = [(team, float(score)) for team, score in sorted_team_scores]
    return ordered_scores

print("Ordered Final Scores:")
print(order_scores_with_teams(calculate_final_scores(scores), {
    'Room_A': ['Team_1', 'Team_2', 'Team_3', 'Team_4', 'Team_5'],
    'Room_B': ['Team_6', 'Team_7', 'Team_8', 'Team_9', 'Team_10']
}))

# Function to normalize scores using z-scores
def normalize_scores(scores):
    normalized_scores = {}
    for room, judges in scores.items():
        room_normalized = []
        for judge, team_scores in judges.items():
            mean = np.mean(team_scores)
            std = np.std(team_scores)
            z_scores = [(score - mean) / std for score in team_scores]
            room_normalized.append(z_scores)
        normalized_scores[room] = np.mean(room_normalized, axis=0)
    return normalized_scores

# Normalize the scores
normalized_scores = normalize_scores(scores)

# Combine Room A and Room B scores into a single DataFrame
teams = ['Team_1', 'Team_2', 'Team_3', 'Team_4', 'Team_5', 'Team_6', 'Team_7', 'Team_8', 'Team_9', 'Team_10']
normalized_df = pd.DataFrame({
    'Team': teams,
    'Normalized_Score': list(normalized_scores['Room_A']) + list(normalized_scores['Room_B'])
})

# Calculate the final average score per team
final_scores = normalized_df.set_index('Team')

# Sort teams by final scores
sorted_final_scores = final_scores.sort_values(by='Normalized_Score', ascending=False)

print("Sorted Final Scores:")
print(sorted_final_scores)
