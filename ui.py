import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector
from database import database

db = database()

db_connection = db.get_database()
# Create the main window
root = tk.Tk()
root.title("Grid Example")
root.geometry("800x600")

# Create a function to retrieve data from the database
def fetch_data(query):
    cursor = db_connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data

# Create a function to populate a grid with data
def populate_grid(grid, query):
    data = fetch_data(query)
    grid.delete(*grid.get_children())  # Clear existing data
    for i, row in enumerate(data, start=1):
        grid.insert("", "end", iid=i, values=row)

# Create the top 5 scores grid
top5_scores_grid = ttk.Treeview(root, columns=("Acao", "Score"))
top5_scores_grid.heading("#0", text="Index")
top5_scores_grid.heading("Acao", text="Acao")
top5_scores_grid.heading("Score", text="Score")
top5_scores_grid.grid(row=0, column=0, padx=10, pady=10)

# Create the top score per setor grid
top_score_per_setor_grid = ttk.Treeview(root, columns=("Setor", "Acao", "Score"))
top_score_per_setor_grid.heading("#0", text="Index")
top_score_per_setor_grid.heading("Setor", text="Setor")
top_score_per_setor_grid.heading("Acao", text="Acao")
top_score_per_setor_grid.heading("Score", text="Score")
top_score_per_setor_grid.grid(row=1, column=0, padx=10, pady=10)

# Create the top volume per setor grid
top_volume_per_setor_grid = ttk.Treeview(root, columns=("Setor", "Acao", "Volume Diario"))
top_volume_per_setor_grid.heading("#0", text="Index")
top_volume_per_setor_grid.heading("Setor", text="Setor")
top_volume_per_setor_grid.heading("Acao", text="Acao")
top_volume_per_setor_grid.heading("Volume Diario", text="Volume Diario")
top_volume_per_setor_grid.grid(row=2, column=0, padx=10, pady=10)

# Define the queries
top5_scores_query = "SELECT acao, score FROM info_acoes ORDER BY score DESC LIMIT 5;"
top_score_per_setor_query = "SELECT setor, acao, score FROM info_acoes " \
                            "WHERE (setor, score) IN (" \
                            "    SELECT setor, MAX(score) " \
                            "    FROM info_acoes " \
                            "    GROUP BY setor" \
                            ");"
top_volume_per_setor_query = "SELECT setor, acao, volume_diario FROM info_acoes " \
                             "WHERE (setor, volume_diario) IN (" \
                             "    SELECT setor, MAX(volume_diario) " \
                             "    FROM info_acoes " \
                             "    GROUP BY setor" \
                             ");"

# Populate the grids with data
populate_grid(top5_scores_grid, top5_scores_query)
populate_grid(top_score_per_setor_grid, top_score_per_setor_query)
populate_grid(top_volume_per_setor_grid, top_volume_per_setor_query)

# Start the main event loop
root.mainloop()

# Close the database connection
db_connection.close()
