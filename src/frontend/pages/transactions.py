import flet as ft


from ui.theme.colors import COLORS
from datetime import datetime
from ui.components.transaction_list import TransactionsList, TransactionItem, CompactTransactionsList

class Transaction:
    def __init__(self, description, montant, categorie, date, icone = "💰"):
        self.description = description
        self.montant = montant
        self.categorie = categorie
        self.date = date
        self.icone = icone

def main(page: ft.Page):
    page.title = "Gestionnaire de Transactions"

    transactions = [
        Transaction("Courses", -40, "Alimentation", datetime(2024, 1, 15), "🛒")
    ]

    #Callback pour les actions
    def on_transaction_click(transaction):
        print(f"Clic sur : {transaction.description}")

    def on_transaction_edit(transaction):
        print(f"Edit sur : {transaction.description}")

    def on_transaction_delete(transaction):
        print(f"Delete sur : {transaction.description}")

    #Créer une liste complète
    transactions_list = TransactionsList(
        transactions=transactions,
        on_transaction_click = on_transaction_click,
        on_transaction_edit = on_transaction_edit,
        on_transaction_delete = on_transaction_delete
    )

    # Créer la iste compoacte pour dashboard
    compact_list = CompactTransactionsList(
        transactions = transactions,
        max_items = 5,
        on_transaction_click = on_transaction_click,
    )

    page.add(
        ft.Text("Liste complète : ", size = 20, weight = ft.FontWeight.BOLD),
        transactions_list.get_container(),
        ft.Divider(),
        ft.Text("Liste compacte : ", size = 20, weight = ft.FontWeight.BOLD),
        compact_list.get_container(),
    )

if __name__ == "__main__":
    ft.app(target=main)