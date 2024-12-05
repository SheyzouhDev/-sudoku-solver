import tkinter as tk
from tkinter import messagebox

MAX_TENTATIVES = 1000  # Nombre maximum de tentatives pour calculer le pourcentage


def afficher_grille(grille, grid_entries):
    """Affiche la grille de Sudoku dans les cases d'entrée."""
    for i in range(9):
        for j in range(9):
            value = grille[i][j]
            grid_entries[i][j].delete(0, tk.END)
            if value != 0:
                grid_entries[i][j].insert(0, str(value))
                grid_entries[i][j].config(state="disabled", disabledbackground="#E8E8E8", disabledforeground="#333333")
            else:
                grid_entries[i][j].config(state="normal", background="#FFFFFF", foreground="#333333")


def est_valide(grille, ligne, col, num):
    """Vérifie si un nombre peut être placé à la position (ligne, col)."""
    for j in range(9):
        if grille[ligne][j] == num:
            return False
    for i in range(9):
        if grille[i][col] == num:
            return False
    start_ligne, start_col = ligne // 3 * 3, col // 3 * 3
    for i in range(3):
        for j in range(3):
            if grille[start_ligne + i][start_col + j] == num:
                return False
    return True


def resoudre_sudoku(grille):
    """Résout le Sudoku en utilisant la méthode de backtracking."""
    for ligne in range(9):
        for col in range(9):
            if grille[ligne][col] == 0:
                for num in range(1, 10):
                    if est_valide(grille, ligne, col, num):
                        grille[ligne][col] = num
                        global tentative_count
                        tentative_count += 1  # Compte une tentative
                        if resoudre_sudoku(grille):
                            return True
                        grille[ligne][col] = 0
                return False
    return True


def get_grille_from_entries(grid_entries):
    """Récupère la grille de Sudoku depuis les champs d'entrée."""
    grille = []
    for i in range(9):
        ligne = []
        for j in range(9):
            try:
                value = int(grid_entries[i][j].get())
                ligne.append(value if value != 0 else 0)
            except ValueError:
                ligne.append(0)
        grille.append(ligne)
    return grille


def on_resoudre_button_click(grid_entries, pourcentage_label, difficulte_label):
    """Gère le clic sur le bouton de résolution."""
    global tentative_count
    tentative_count = 0  # Réinitialiser le compteur
    grille = get_grille_from_entries(grid_entries)
    if resoudre_sudoku(grille):
        afficher_grille(grille, grid_entries)
        mettre_a_jour_pourcentage_et_difficulte(pourcentage_label, difficulte_label)
    else:
        messagebox.showerror("Erreur", "Aucune solution trouvée!")


def mettre_a_jour_pourcentage_et_difficulte(pourcentage_label, difficulte_label):
    """Met à jour le score en pourcentage et la difficulté."""
    pourcentage = max(0, (1 - tentative_count / MAX_TENTATIVES) * 100)
    pourcentage_label.config(text=f"Score : {pourcentage:.2f} %")

    # Déterminer la difficulté
    if tentative_count <= 100:
        difficulte = "Débutant"
    elif tentative_count <= 300:
        difficulte = "Facile"
    elif tentative_count <= 600:
        difficulte = "Intermédiaire"
    elif tentative_count <= 999:
        difficulte = "Difficile"
    else:
        difficulte = "Impossible"

    difficulte_label.config(text=f"Difficulté : {difficulte}")


def reset_grille(grid_entries, pourcentage_label, difficulte_label):
    """Réinitialise la grille de Sudoku."""
    for i in range(9):
        for j in range(9):
            grid_entries[i][j].delete(0, tk.END)
            grid_entries[i][j].config(state="normal", background="#FFFFFF", foreground="#333333")
    pourcentage_label.config(text="Score : -")
    difficulte_label.config(text="Difficulté : -")


def valider_saisie(action, valeur, row, col, grid_entries):
    """Valide la saisie pour n'accepter qu'un seul chiffre entre 0 et 9, et change automatiquement de case."""
    if action == "1":  # Action = 1 signifie une tentative d'ajout
        if valeur.isdigit() and 0 <= int(valeur) <= 9:
            if valeur == "0":
                grid_entries[row][col].delete(0, tk.END)
            focus_suivant(row, col, grid_entries)
            return True
        return False
    return True


def focus_suivant(row, col, grid_entries):
    """Déplace le focus vers la case suivante."""
    row, col = int(row), int(col)  # Assure que row et col sont bien des entiers
    if col < 8:
        grid_entries[row][col + 1].focus_set()
    elif row < 8:
        grid_entries[row + 1][0].focus_set()
    else:
        grid_entries[0][0].focus_set()


def creer_fenetre():
    """Crée la fenêtre Tkinter avec un design équilibré."""
    root = tk.Tk()
    root.title("Résolveur de Sudoku")
    root.configure(bg="#F9F9F9")  # Couleur de fond globale

    grid_entries = []

    # Étiquette pour le pourcentage
    pourcentage_label = tk.Label(root, text="Score : -", font=("Helvetica", 14), bg="#F9F9F9", fg="#333333")
    pourcentage_label.grid(row=0, column=0, pady=(10, 0), columnspan=2)

    # Étiquette pour la difficulté
    difficulte_label = tk.Label(root, text="Difficulté : -", font=("Helvetica", 12), bg="#F9F9F9", fg="#555555")
    difficulte_label.grid(row=1, column=0, pady=(5, 10), columnspan=2)

    # Frame pour la grille
    frame = tk.Frame(root, bg="#F9F9F9", padx=10, pady=10)
    frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

    # Construction de la grille de 9x9
    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = tk.Entry(frame, width=3, font=("Helvetica", 18), justify="center", validate="key",
                             validatecommand=(root.register(lambda action, valeur, row=i, col=j: valider_saisie(action, valeur, row, col, grid_entries)), "%d", "%P"))
            entry.grid(row=i, column=j, padx=(2 if j % 3 == 0 else 1), pady=(2 if i % 3 == 0 else 1))
            entry.configure(
                relief="flat",
                highlightbackground="#CCCCCC", highlightthickness=1,
                bg="#FFFFFF", fg="#333333", insertbackground="#333333"
            )
            row_entries.append(entry)
        grid_entries.append(row_entries)

    # Frame pour les boutons
    button_frame = tk.Frame(root, bg="#F9F9F9")
    button_frame.grid(row=3, column=0, pady=10, columnspan=2)

    # Bouton pour résoudre
    resolver_button = tk.Button(button_frame, text="Résoudre", font=("Helvetica", 14), bg="#4CAF50", fg="white",
                                 activebackground="#45A049", activeforeground="white",
                                 command=lambda: on_resoudre_button_click(grid_entries, pourcentage_label, difficulte_label))
    resolver_button.grid(row=0, column=0, padx=10)

    # Bouton pour réinitialiser
    reset_button = tk.Button(button_frame, text="Réinitialiser", font=("Helvetica", 14), bg="#F44336", fg="white",
                              activebackground="#E53935", activeforeground="white",
                              command=lambda: reset_grille(grid_entries, pourcentage_label, difficulte_label))
    reset_button.grid(row=0, column=1, padx=10)

    return root, grid_entries


# Exécution principale
if __name__ == "__main__":
    tentative_count = 0  # Compteur de tentatives global
    fenetre, grid_entries = creer_fenetre()
    fenetre.mainloop()
