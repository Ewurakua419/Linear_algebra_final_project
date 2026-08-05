import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class Players:

    def __init__(self, file="synthetic_players.csv", num=0):
        # np.set_printoptions(suppress=True, precision=2)
        # self.file=file
        # encoding = {
        #             'GK': 0,
        #             'CM': 1,
        #             'CAM': 2,
        #             'FB': 3,
        #             'CB': 4,
        #             'ST': 5
        #         }

        # """if num==0:
        #     self.df = pd.read_csv("synthetic_players.csv")
        # else:
        #     self.df = pd.read_csv(
        #         "synthetic_players.csv",
        #         nrows=num,
        #     )"""

        # try:
        #     with open(str(self.file), "r") as file:
        #         if num==0:
        #             self.df = pd.read_csv(file)
        #         else:
        #             self.df = pd.read_csv(file, nrows=num)

        #         # create a new column to house the encoded positions.
        #         print("Success")

        # except FileNotFoundError:
        #     if num==0:
        #         self.df = pd.read_csv("synthetic_players.csv")
        #     else:
        #         self.df = pd.read_csv("synthetic_players.csv", nrows=num, header=0)
        #     print(f"Error: The file {self.file} does not exist. We shall use synthetic data")

        # self.df['position_encoded'] = self.df['position'].map(encoding)

        # # the column names might not be the same across different data sets
        # self.matrix_df = self.df[
        #                 [
        #                     "pace",
        #                     "dribbling",
        #                     "passing_accuracy",
        #                     "shooting",
        #                     "tackling",
        #                     "aerial_duels_won_pct",
        #                     "positioning",
        #                     "stamina",
        #                     "goals_per90",
        #                     "assists_per90",
        #                     "estimated_value_eur_m",
        #                 ]
        #             ]
        # self.matrix_df=self.matrix_df.columns.str.strip()

        # self.matrix_df = self.matrix_df.fillna(0)
        # self.matrix = self.matrix_df.to_numpy()

        np.set_printoptions(suppress=True, precision=2)
        self.file=file

        self.df = pd.read_csv("synthetic_players.csv", nrows=num, header=0)

        encoding = {
                    'GK': 0,
                    'CM': 1,
                    'CAM': 2,
                    'FB': 3,
                    'CB': 4,
                    'ST': 5
                }

        self.matrix_df = self.df[
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

        self.df['position_encoded'] = self.df['position'].map(encoding)

        self.matrix_df.columns = self.matrix_df.columns.str.strip()
        self.matrix_df = self.matrix_df.fillna(0)
        self.euclidean_distance()

    def euclidean_distance(self):
        
        self.matrix = self.matrix_df.to_numpy()

        self.euclidean_matrix = np.zeros((len(self.matrix), len(self.matrix)))
        position_distance = np.array(
            [
                # GK CM CAM FB CB ST
                [0, 4, 4, 4, 3, 4],  # GK
                [4, 0, 1, 2, 3, 2],  # CM
                [4, 1, 0, 3, 4, 1],  # CAM
                [4, 2, 3, 0, 1, 4],  # FB
                [3, 3, 4, 1, 0, 4],  # CB
                [4, 2, 1, 4, 4, 0],  # ST
            ]
        )
        position_weight = 10

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                # difference between a given row and the remaining rows
                difference = self.matrix[i] - self.matrix[j]

                total = 0

                # calculate the total of square of the differennce value
                # basically accomplishin (x2 - x1)**2 + (y2 - y1)**2
                for value in difference:
                    total += pow(value, 2)
                euclidean_distance = math.sqrt(total)

                # get the encoded version of the position of both players.
                player1_position = self.df.loc[i, "position_encoded"]
                player2_position = self.df.loc[j, "position_encoded"]

                # obtain the penalty from the positon distance matrix.
                position_penalty = position_distance[player1_position][player2_position] # type: ignore

                self.euclidean_matrix[i][j] = euclidean_distance + position_weight * position_penalty #add the position penalty with a weight to the final euclidian distance.

        self.euclidean_matrix_pd = pd.DataFrame(
            data=self.euclidean_matrix, columns=self.df["name"].to_numpy()
        )
        self.euclidean_matrix_pd["name"]=self.df["name"]
        self.euclidean_matrix_pd = self.euclidean_matrix_pd.dropna(axis=1, how="all")
        self.euclidean_matrix_pd = self.euclidean_matrix_pd.dropna(axis=0)  # , how="all"

    def get_player_names(self):
        return self.df["name"].tolist()
    
    def comparism(self):
        sns.heatmap(
            self.euclidean_matrix_pd.loc[:, self.euclidean_matrix_pd.columns != "name"],
            annot=True,
            fmt = ".0f",
            cmap="coolwarm",
            xticklabels=self.euclidean_matrix_pd[["name"]].to_numpy(),
            yticklabels=self.euclidean_matrix_pd[["name"]].to_numpy(),
        )
        return plt.show()

    def mostsimn(self, row, num):
        numeric_row = pd.to_numeric(row, errors='coerce').astype(float)
        
        # Filter out 0 values
        non_zero = numeric_row[numeric_row != 0]
        # Get the 3 smallest values and their column names
        smallest = non_zero.nsmallest(num)

        # Format the result as a list of "Column: Value" strings
        return [f"{col}" for col, val in smallest.items()]

    def similarity(self, num=3):
        try:
            # most similar num rather
            self.euclidean_matrix_pd[f"most similar {num}"] = self.euclidean_matrix_pd.apply(
                lambda row: self.mostsimn(row=row, num=num), axis=1
            )
            self.similar3 = pd.DataFrame(
                {"player": self.euclidean_matrix_pd[["name"]].to_numpy().flatten(), "most similar": self.euclidean_matrix_pd[f"most similar {num}"]}
            )
            return self.similar3
        except Exception as e:
            print(f"Error calculating similarities: {e}")
            return None

    def similar_to(self, player_name, num=3):
        try:
            # Find the player's row
            player_row = self.euclidean_matrix_pd[
                self.euclidean_matrix_pd["name"] == player_name
            ]

            if player_row.empty:
                print(f"Player '{player_name}' not found.")
                return None

            # Get the actual row
            row = player_row.iloc[0]

            # Reuse the similarity calculation
            return self.mostsimn(row, num)

        except Exception as e:
            print(f"Error finding similar players: {e}")
            return None

    def get_player_stats(self, player_name):
        player = self.df[self.df["name"] == player_name]

        if player.empty:
            return None

        player =  player.iloc[0]

        return {
            "info": {
                "age": int(player["age"]),
                "position": player["position"],
                "league": player["league"],
                "nationality": player["nationality"],
                "value": float(player["estimated_value_eur_m"])
            },

            "stats": {
                "pace": float(player["pace"]),
                "dribbling": float(player["dribbling"]),
                "passing_accuracy": float(player["passing_accuracy"]),
                "shooting": float(player["shooting"]),
                "tackling": float(player["tackling"]),
                "aerial_duels_won_pct": float(player["aerial_duels_won_pct"]),
                "positioning": float(player["positioning"]),
                "stamina": float(player["stamina"]),
                "goals_per90": float(player["goals_per90"]),
                "assists_per90": float(player["assists_per90"])
            }
        }
    
    # def similarity(self, num=3):
    #     # Ensure the similarity matrix exists
    #     if self.euclidean_matrix_pd is None or self.euclidean_matrix_pd.empty:
    #         return None
            
    #     try:
    #         results = {}
            
    #         # Iterate safely through each player's distance row
    #         for player_name in self.euclidean_matrix_pd.index:
    #             row = self.euclidean_matrix_pd.loc[player_name]
                
    #             # FIXED: Drop the player's own row label so they don't match with themselves
    #             # This safely keeps valid '0' distances from other identical players
    #             clean_row = row.drop(labels=[player_name], errors='ignore')
                
    #             # Find the N smallest distances (the closest matches)
    #             smallest = clean_row.nsmallest(num)
                
    #             # Store the names of the closest matching players
    #             results[player_name] = [f"{col}" for col in smallest.index]
                
    #         # Convert the dictionary cleanly into your final tracking DataFrame
    #         self.similar3 = pd.DataFrame({
    #             "player": list(results.keys()),
    #             "most similar": list(results.values())
    #         })
            
    #         return self.similar3
            
    #     except Exception as e:
    #         print(f"Error calculating similarities: {e}")  # Helpful debugging feedback
    #         return None

        

    def remove(self, name):# remove a player we have used
        if name in self.euclidean_matrix_pd["name"]:
            self.curr_matrix=self.euclidean_matrix_pd.drop(columns=[name])
            self.curr_matrix = self.curr_matrix[self.curr_matrix["name"] != name]
            return self.curr_matrix

    def similarity_matrix(self, matrix,num=3): #do a new similarity check 
        try:
            matrix["most similar 3"] = self.euclidean_matrix_pd.apply(
                    lambda row: self.mostsimn(row=row, num=num), axis=1
                )
            similar3 = pd.DataFrame(
                    {"player": matrix[["name"]].to_numpy().flatten(), "most similar":matrix["most similar 3"]}
                )
            return similar3
        except:
            print("Please ensure that the matrix has the correct structure")
            return None


    def display_graph(self, p1, p2):

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

        p1_data = self.df[self.df['name'].str.lower() == p1.lower()]
        p2_data = self.df[self.df['name'].str.lower() == p2.lower()]

        p1_values = p1_data[categories].iloc[0].tolist()
        p2_values = p2_data[categories].iloc[0].tolist()

        p1_values += p1_values[:1]
        p2_values += p2_values[:1]

        
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


    def create_radar_chart(self, p1, p2):

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

        p1_data = self.df[self.df['name'].str.lower() == p1.lower()]
        p2_data = self.df[self.df['name'].str.lower() == p2.lower()]

        p1_values = p1_data[categories].iloc[0].tolist()
        p2_values = p2_data[categories].iloc[0].tolist()

        p1_values += p1_values[:1]
        p2_values += p2_values[:1]

        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
        ax.set_thetagrids(np.degrees(angles[:-1]), categories, color='grey', size=10)
        ax.set_rlabel_position(0)

        plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="grey", size=7)
        plt.ylim(0, 100)

        # 5. Plot Player 1 (Teal Line + Dots)
        ax.plot(angles, p1_values, color="#D2042D", linewidth=2, marker='o', label=p1)
        ax.fill(angles, p1_values, color="#D2042D", alpha=0.1)

        # 6. Plot Player 2 (Purple Line + Dots)
        ax.plot(angles, p2_values, color="#2931A4", linewidth=2, marker='o', label=p2)
        ax.fill(angles, p2_values, color="#2931A4", alpha=0.1)

        # Add Legend
        plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

        buffer = BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight")
        buffer.seek(0)
        image = base64.b64encode(buffer.read()).decode()
        buffer.close()
        plt.close(fig)

        return image







      
