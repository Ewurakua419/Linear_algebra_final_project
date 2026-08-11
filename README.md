# Linear Algebra Final Project
## Group 10 - Lois FC

### Members
Ewurakua Amoah - 74492028
Haris Issah - 41942028
Gabriel Akurang -  35882028

### Description

This project is a **Player Similarity System** designed to evaluate and quantify how similar a football player is to others based on key performance metrics (e.g., shooting, stamina, passing). This system serves as a tool for sports analytics and talent scouting, allowing scouts to find alternative targets or rank players dynamically by profile mapping.

*   **Mathematical Concept**: Player attributes are represented as vectors ($1\times N$ row arrays). The system calculates the **Euclidean Distance** between these feature vectors to determine mathematical similarity:
    $$d(\mathbf{p_1}, \mathbf{p_2}) = \sqrt{\sum_{i=1}^{n} (p_{1i} - p_{2i})^2}$$
*   **Ranking**: Players are ranked globally based on their similarity score; a lower distance value indicates a higher likeness to the target profile.
*   **Visualizations**: 
    *   A **General Heatmap** representing the distance matrix across all players in the dataset.
    *   A **Radar Chart** overlaying two selected players to visually compare attribute overlaps and gaps.

###  Repository Structure

The core files driving this repository include:
*   `app.py`: The main entry point script for the system.
*   `synthetic_players.csv`: The core dataset containing the attributes matrix for evaluation.
*   `concepts.py` / `players.py` / `driver.py`: Supporting logic processing mathematical data arrays and distances.
*   `templates/`: UI layout or rendering configurations if utilized via a framework dashboard.

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Ewurakua419/Linear_algebra_final_project.git 
    cd Linear_algebra_final_project
    ```
2.  **Ensure Python is Installed**:
    Make sure you have Python 3.8 or higher installed on your computer.

3.  **Install Required Mathematical & Plotting Libraries**:
    Run the following command to install the specific libraries needed for array calculations, data handling, and visual generation:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  **Prepare the Dataset**:
    The player attributes file ( `synthetic_players.csv`) is placed in the project root folder.

2.  **Run the System**:
    Execute the main script to compute the Euclidean distance matrix, print the ranked similarity outputs, and view the visual plots:
    ```bash
    python app.py
    ```
3.  **System Functionality**:
    *   The app ingests player row arrays directly from `synthetic_players.csv`.
    *   It generates a global Euclidean distance heatmap.
    *   It allows users to select players to render overlapping geometric radar charts for instant similarity diagnostics.
