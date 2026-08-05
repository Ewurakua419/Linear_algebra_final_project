import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt

# This is to ensure the matrix values are in an integer format
np.set_printoptions(suppress=True, precision=2)

# the data is loaded into a data frame for analysis
# you need to put the csv file path here
df = pd.read_csv(
    "synthetic_players.csv",
    nrows=15,
) #"/Users/Takyi/Desktop/ISEHSA/year2sem2/linear algebra/synthetic_players.csv",


# print(df.head())

# this is the variables of the data not included for the matrix (like name, country, age, etc)
# temp_df = df[['player_id', 'name','position','age','nationality','league']]
# print(temp_df.head())

# columns needed for the matrix formation (numeric)
# contains nnull values not yet worked on
matrix_df = df[
    [
        "pace",
        "dribbling",
        "passing_accuracy",
        "shooting",
        "tackling",
        "aerial_duels_won_pct",
        "positioning",
        "stamina",
        "goals_per90",
        "assists_per90",
        "estimated_value_eur_m",
    ]
]

# collect the names of the list of players
player_names = df['name'].tolist()

# encode the positions to integers, based on where they lie in the position matrix
encoding = {
    'GK': 0,
    'CM': 1,
    'CAM': 2,
    'FB': 3,
    'CB': 4,
    'ST': 5
}

# create a new column to house the encoded positions.
df['position_encoded'] = df['position'].map(encoding)

matrix_df.columns = matrix_df.columns.str.strip()
matrix_df = matrix_df.fillna(0)


# convert the data to a matrix format
# each row contains a player's attribute.

matrix = matrix_df.to_numpy()

# initiliaze the size of the final matrix containing euclidean values

euclidean_matrix = np.zeros((len(matrix), len(matrix)))

position_distance = np.array([
    # GK CM CAM FB CB ST
    [0, 4, 4, 4, 3, 4],  # GK
    [4, 0, 1, 2, 3, 2],  # CM
    [4, 1, 0, 3, 4, 1],  # CAM
    [4, 2, 3, 0, 1, 4],  # FB
    [3, 3, 4, 1, 0, 4],  # CB
    [4, 2, 1, 4, 4, 0],  # ST
])

position_weight = 2

# to loop through the matrix for a given row
for i in range(len(matrix)):
    for j in range(len(matrix)):
        # difference between a given row and the remaining rows
        difference = matrix[i] - matrix[j]

        total = 0

        # calculate the total of square of the differennce value
        # basically accomplishin (x2 - x1)**2 + (y2 - y1)**2
        for value in difference:
            total += pow(value, 2)

        # priority is given to positional similarity by
        # giving players in matching positions an advantage,
        # even though superior players from other positions can still outrank them.

        # NOTE: what would be required? the position, then looking it up in the matrix, and then adding it to the euclidian distance

        # get the euclidean value
        euclidean_distance = math.sqrt(total)

        # get the encoded version of the position of both players.
        player1_position = df.loc[i, "position_encoded"]
        player2_position = df.loc[j, "position_encoded"]

        # obtain the penalty from the positon distance matrix.
        position_penalty = position_distance[player1_position][player2_position] # type: ignore

        euclidean_matrix[i][j] = euclidean_distance + position_weight * position_penalty #add the position penalty with a weight to the final euclidian distance.

        # the weight can be adjusted based on how important we want the position to be.

# show the values in the terminal
# print(euclidean_matrix)

# euclidean_matrix_clean =np.nan_to_num(euclidean_matrix, nan=-1)

# heatmap implementation
sns.heatmap(
    euclidean_matrix,
    annot=True,
    fmt =".0f",
    cmap="coolwarm",
    xticklabels=df[["name"]].to_numpy(),
    yticklabels=df[["name"]].to_numpy(),
)


# plt.show()

euclidean_matrix_pd = pd.DataFrame(
    data=euclidean_matrix, columns=df[["name"]].to_numpy()
)

names = df[["name"]].to_numpy()
names=names[:11]
print(names)
euclidean_matrix_pd = euclidean_matrix_pd.dropna(axis=1, how="all")
euclidean_matrix_pd = euclidean_matrix_pd.dropna(axis=0, how="all")
print(euclidean_matrix_pd)

euclidean_matrix_pd_nan=euclidean_matrix_pd.mask(euclidean_matrix_pd==0)
# similar=pd.DataFrame({
#     "player":names.flatten(),
#     "most similar": euclidean_matrix_pd_nan.idxmin(axis=1)

# })
# print(similar)


# def mostsimn(row, num=3):
#     # Filter out 0 values
#     non_zero = row[row != 0]
#     # Get the 3 smallest values and their column names
#     smallest = non_zero.nsmallest(num)

#     # Format the result as a list of "Column: Value" strings
#     return [f"{col}" for col, val in smallest.items()]

# euclidean_matrix_pd["most similar 3"] = euclidean_matrix_pd.apply(lambda row: mostsimn(row=row,num=2), axis=1)
# similar3 = pd.DataFrame(
#     {"player": names.flatten(), "most similar": euclidean_matrix_pd["most similar 3"]}
# )
# print(similar3)

# Apply the function across each row
# #Radar chart GUIDE

# import numpy as np
# import matplotlib.pyplot as plt

# # 1. Define your metrics (the axes labels around the circle)
# categories = [
#     'Final Product', 'Shooting Volume', 'Own Shot Gen', 'Finishing Quality',
#     'Creation Passes', 'Creation Carries', 'Dribbling', 'Progression',
#     'Pass Accuracy', 'Active Defending', 'Total VAEP'
# ]
# num_vars = len(categories)

# # 2. Split the circle into equal angles for each metric
# angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# # The radar chart needs to "close the loop", so append the start value to the end
# angles += angles[:1]

# # 3. Add data for both profiles (e.g., Estêvão vs Jamie Gittens)
# # Values should range from 0 to 100 for percentiles
# player_1_data = [96, 92, 97, 58, 72, 99, 99, 82, 48, 80, 99]
# player_2_data = [53, 14, 21, 11, 75, 91, 91, 58, 46, 79, 46]

# player_1_data += player_1_data[:1]
# player_2_data += player_2_data[:1]

# # 4. Initialize the plot with dark styling matching your image
# plt.style.use('dark_background')
# fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# # Draw one axe per variable and add labels
# plt.xticks(angles[:-1], categories, color='grey', size=10)

# # Draw y-axis gridlines (percentile rings from 0 to 100)
# ax.set_rlabel_position(0)
# plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="grey", size=7)
# plt.ylim(0, 100)

# # 5. Plot Player 1 (Teal Line + Dots)
# ax.plot(angles, player_1_data, color='#00ffcc', linewidth=2, marker='o', label='Estêvão')
# ax.fill(angles, player_1_data, color='#00ffcc', alpha=0.1)

# # 6. Plot Player 2 (Purple Line + Dots)
# ax.plot(angles, player_2_data, color='#cc66ff', linewidth=2, marker='o', label='Jamie Gittens')
# ax.fill(angles, player_2_data, color='#cc66ff', alpha=0.1)

# # Add Legend
# plt.legend(loc='upper right', bbox_transform=fig.transFigure)

# plt.show()


def display_graph(p1, p2):

    categories = [
                        
                    "pace",
                    "dribbling",
                    "passing_accuracy",
                    "shooting",
                    "tackling",
                    "aerial_duels_won_pct",
                    "positioning",
                    "stamina",
                    "goals_per90",
                    "assists_per90",
                    "estimated_value_eur_m" ]


    num_vars = len(categories)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    angles += angles[:1]

    p1_data = df[df['name'].str.lower() == p1.lower()]
    p2_data = df[df['name'].str.lower() == p2.lower()]

    p1_values = p1_data[categories].iloc[0].tolist()
    p2_values = p2_data[categories].iloc[0].tolist()

    p1_values += p1_values[:1]
    p2_values += p1_values[:1]

    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
    ax.set_thetagrids(np.degrees(angles[:-1]), categories, color='grey', size=10)
    ax.set_rlabel_position(0)

    plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="grey", size=7)
    plt.ylim(0, 100)

    # 5. Plot Player 1 (Teal Line + Dots)
    ax.plot(angles, p1_values, color="#7a9d2e", linewidth=2, marker='o', label=p1)
    ax.fill(angles, p1_values, color="#7a9d2e", alpha=0.1)

    # 6. Plot Player 2 (Purple Line + Dots)
    ax.plot(angles, p2_values, color="#2931A4", linewidth=2, marker='o', label=p2)
    ax.fill(angles, p2_values, color="#2931A4", alpha=0.1)

    # Add Legend
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    plt.show()



# display_graph("Thiago Kone","Erik Smith")




