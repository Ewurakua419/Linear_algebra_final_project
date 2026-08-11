from players import Players

player_instance = Players()
num = 20
# To display the row vectors for all players
print(player_instance.original_player_vectors(num))
print()

# To display the scaled row vectors for n players
print(player_instance.scaled_player_vectors(num))
print()

# To display the euclidean distance value for the players
matrix_data = player_instance.get_euclidean_matrix()
print(matrix_data.iloc[:, :])
