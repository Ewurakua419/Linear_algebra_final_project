import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt

class Players:

    def __init__(self, file="synthetic_players.csv", num=0):
        np.set_printoptions(suppress=True, precision=2)
        self.file=file
        encoding = {
                    'GK': 0,
                    'CM': 1,
                    'CAM': 2,
                    'FB': 3,
                    'CB': 4,
                    'ST': 5
                }

        """if num==0:
            self.df = pd.read_csv("synthetic_players.csv")
        else:
            self.df = pd.read_csv(
                "synthetic_players.csv",
                nrows=num,
            )"""

        try:
            with open(str(self.file), "r") as file:
                if num==0:
                    self.df = pd.read_csv(file)
                else:
                    self.df = pd.read_csv(file, nrows=num)

                # create a new column to house the encoded positions.
                print("Success")

        except FileNotFoundError:
            if num==0:
                self.df = pd.read_csv("synthetic_players.csv")
            else:
                self.df = pd.read_csv("synthetic_players.csv", nrows=num, header=0)
            print(f"Error: The file {self.file} does not exist. We shall use synthetic data")

        self.df['position_encoded'] = self.df['position'].map(encoding)
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
        self.matrix_df=self.matrix_df.columns.str.strip()

    def euclidean_distance(self):
        self.matrix = self.matrix_df.to_numpy(dtype =float)
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
        position_weight = 2

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
            data=self.euclidean_matrix, columns=self.df[["name"]].to_numpy()
        )
        self.euclidean_matrix_pd["name"]=self.df["name"]
        self.euclidean_matrix_pd = self.euclidean_matrix_pd.dropna(axis=1, how="all")
        self.euclidean_matrix_pd = self.euclidean_matrix_pd.dropna(axis=0)  # , how="all"

    def comparism(self):
        sns.heatmap(
            self.euclidean_matrix_pd.loc[:, self.euclidean_matrix_pd.columns != "name"],
            annot=True,
            cmap="coolwarm",
            xticklabels=self.euclidean_matrix_pd[["name"]].to_numpy(),
            yticklabels=self.euclidean_matrix_pd[["name"]].to_numpy(),
        )
        return plt.show()

    def similarity(self, num=3):
        def mostsimn(row, num=num):
            # Filter out 0 values
            non_zero = row[row != 0]
            # Get the 3 smallest values and their column names
            smallest = non_zero.nsmallest(num)

            # Format the result as a list of "Column: Value" strings
            return [f"{col}" for col, val in smallest.items()]
        try:
            self.euclidean_matrix_pd["most similar 3"] = self.euclidean_matrix_pd.apply(
                lambda row: mostsimn(row=row, num=num), axis=1
            )
            self.similar3 = pd.DataFrame(
                {"player": self.euclidean_matrix_pd[["name"]].to_numpy().flatten(), "most similar": self.euclidean_matrix_pd["most similar 3"]}
            )
            return self.similar3
        except:
            return None

    def remove(self, name):# remove a player weve used
        if name in self.euclidean_matrix_pd["name"]:
            self.curr_matrix=self.euclidean_matrix_pd.drop(columns=[name])
            self.curr_matrix = self.curr_matrix[self.curr_matrix["name"] != name]
            return self.curr_matrix

    def similarity_matrix(self, matrix,num=3): #do a new similarity check 
        def mostsimn(row, num=num):
            # Filter out 0 values
            non_zero = row[row != 0]
            # Get the 3 smallest values and their column names
            smallest = non_zero.nsmallest(num)

            # Format the result as a list of "Column: Value" strings
            return [f"{col}" for col, val in smallest.items()]
        try:
            matrix["most similar 3"] = self.euclidean_matrix_pd.apply(
                    lambda row: mostsimn(row=row, num=num), axis=1
                )
            similar3 = pd.DataFrame(
                    {"player": matrix[["name"]].to_numpy().flatten(), "most similar":matrix["most similar 3"]}
                )
            return similar3
        except:
            print("Please ensure that the matrix has the correct structure")
            return None
