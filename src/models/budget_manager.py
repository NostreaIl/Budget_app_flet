# src/models/budget_manager.py - Gestionnaire principal de budget
"""
Gestionnaire de budget principal - Port du BudgetManager C++
Gère les transactions, catégories et statistiques
"""

import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Transaction:
    """Modèle de transaction simplifié"""
    id: int
    description: str
    montant: float
    categorie: str
    date: datetime
    icone: str = "💰"

    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire pour la sérialisation"""
        return {
            'id': self.id,
            'description': self.description,
            'montant': self.montant,
            'categorie': self.categorie,
            'date': self.date.isoformat(),
            'icone': self.icone
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Crée une transaction depuis un dictionnaire"""
        return cls(
            id=data['id'],
            description=data['description'],
            montant=data['montant'],
            categorie=data['categorie'],
            date=datetime.fromisoformat(data['date']),
            icone=data.get('icone', '💰')
        )


@dataclass
class CategoryBudget:
    """Modèle de catégorie de budget"""
    id: int
    nom: str
    budget_mensuel: float
    couleur: str
    icone: str = "📁"
    actif: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire pour la sérialisation"""
        return {
            'id': self.id,
            'nom': self.nom,
            'budget_mensuel': self.budget_mensuel,
            'couleur': self.couleur,
            'icone': self.icone,
            'actif': self.actif
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CategoryBudget':
        """Crée une catégorie depuis un dictionnaire"""
        return cls(
            id=data['id'],
            nom=data['nom'],
            budget_mensuel=data['budget_mensuel'],
            couleur=data['couleur'],
            icone=data.get('icone', '📁'),
            actif=data.get('actif', True)
        )


class BudgetManager:
    """
    Gestionnaire principal de budget
    Port du BudgetManager C++ vers Python
    """

    def __init__(self, data_directory: str = None):
        """
        Initialise le gestionnaire de budget

        Args:
            data_directory: Répertoire pour les données (optionnel)
        """
        self.data_directory = data_directory or self._get_default_data_directory()
        self._ensure_data_directory()

        # Collections principales
        self.transactions: List[Transaction] = []
        self.categories_budgets: List[CategoryBudget] = []

        # Compteurs
        self._next_transaction_id = 1
        self._next_category_id = 1

        # État
        self.has_demo_data = False

        # Initialisation
        self._initialize_demo_data()

    def _get_default_data_directory(self) -> str:
        """Retourne le répertoire par défaut pour les données"""
        home_dir = Path.home()
        app_dir = home_dir / "BudgetApp_NatureTech"
        return str(app_dir)

    def _ensure_data_directory(self):
        """S'assure que le répertoire de données existe"""
        Path(self.data_directory).mkdir(parents=True, exist_ok=True)

    def _initialize_demo_data(self):
        """Initialise les données de démonstration"""
        # Catégories de démonstration
        self.categories_budgets = [
            CategoryBudget(1, "Alimentation", 400.0, "#4ECDC4", "🍽️"),
            CategoryBudget(2, "Transport", 200.0, "#FFE66D", "🚗"),
            CategoryBudget(3, "Loisirs", 150.0, "#9C27B0", "🎮"),
            CategoryBudget(4, "Salaire", 3000.0, "#00E5FF", "💼"),
            CategoryBudget(5, "Factures", 500.0, "#FF6B6B", "🧾"),
        ]
        self._next_category_id = 6

        # Transactions de démonstration
        self.transactions = [
            Transaction(1, "Salaire mensuel", 2500.0, "Salaire", datetime(2024, 12, 1), "💼"),
            Transaction(2, "Courses Carrefour", -85.50, "Alimentation", datetime(2024, 12, 15), "🛒"),
            Transaction(3, "Plein d'essence", -65.00, "Transport", datetime(2024, 12, 14), "⛽"),
            Transaction(4, "Restaurant", -45.80, "Alimentation", datetime(2024, 12, 13), "🍽️"),
            Transaction(5, "Netflix", -15.99, "Loisirs", datetime(2024, 12, 12), "📺"),
            Transaction(6, "Électricité", -120.0, "Factures", datetime(2024, 12, 10), "⚡"),
            Transaction(7, "Remboursement", 50.0, "Salaire", datetime(2024, 12, 9), "💰"),
            Transaction(8, "Supermarché", -78.30, "Alimentation", datetime(2024, 12, 8), "🛍️"),
            Transaction(9, "Cinéma", -24.00, "Loisirs", datetime(2024, 12, 7), "🎬"),
            Transaction(10, "Métro mensuel", -75.20, "Transport", datetime(2024, 12, 5), "🚇"),
        ]
        self._next_transaction_id = 11
        self.has_demo_data = True

    def get_solde(self) -> float:
        """Calcule le solde total"""
        return sum(t.montant for t in self.transactions)

    def get_revenus_total(self) -> float:
        """Calcule le total des revenus"""
        return sum(t.montant for t in self.transactions if t.montant > 0)

    def get_depenses_total(self) -> float:
        """Calcule le total des dépenses (valeur absolue)"""
        return sum(abs(t.montant) for t in self.transactions if t.montant < 0)

    @property
    def nombre_transactions(self) -> int:
        """Nombre total de transactions"""
        return len(self.transactions)

    def add_transaction(self, description: str, montant: float, categorie: str,
                        date_transaction: datetime = None, icone: str = "💰") -> Transaction:
        """
        Ajoute une nouvelle transaction

        Args:
            description: Description de la transaction
            montant: Montant (positif pour revenus, négatif pour dépenses)
            categorie: Nom de la catégorie
            date_transaction: Date de la transaction (maintenant par défaut)
            icone: Icône de la transaction

        Returns:
            Transaction: Transaction créée
        """
        if date_transaction is None:
            date_transaction = datetime.now()

        transaction = Transaction(
            id=self._next_transaction_id,
            description=description,
            montant=montant,
            categorie=categorie,
            date=date_transaction,
            icone=icone
        )

        self.transactions.append(transaction)
        self._next_transaction_id += 1

        return transaction

    def add_category(self, nom: str, budget_mensuel: float, couleur: str,
                     icone: str = "📁") -> CategoryBudget:
        """
        Ajoute une nouvelle catégorie

        Args:
            nom: Nom de la catégorie
            budget_mensuel: Budget mensuel alloué
            couleur: Couleur de la catégorie
            icone: Icône de la catégorie

        Returns:
            CategoryBudget: Catégorie créée
        """
        category = CategoryBudget(
            id=self._next_category_id,
            nom=nom,
            budget_mensuel=budget_mensuel,
            couleur=couleur,
            icone=icone
        )

        self.categories_budgets.append(category)
        self._next_category_id += 1

        return category

    def get_transactions_by_category(self, category_name: str) -> List[Transaction]:
        """
        Retourne les transactions d'une catégorie

        Args:
            category_name: Nom de la catégorie

        Returns:
            List[Transaction]: Liste des transactions de la catégorie
        """
        return [t for t in self.transactions if t.categorie == category_name]

    def get_monthly_summary(self, year: int = None, month: int = None) -> Dict[str, Any]:
        """
        Retourne un résumé mensuel

        Args:
            year: Année (année courante par défaut)
            month: Mois (mois courant par défaut)

        Returns:
            Dict: Résumé avec revenus, dépenses, solde et nombre de transactions
        """
        now = datetime.now()
        target_year = year or now.year
        target_month = month or now.month

        # Filtrer les transactions du mois
        monthly_transactions = [
            t for t in self.transactions
            if t.date.year == target_year and t.date.month == target_month
        ]

        revenus = sum(t.montant for t in monthly_transactions if t.montant > 0)
        depenses = sum(abs(t.montant) for t in monthly_transactions if t.montant < 0)

        return {
            'revenus': revenus,
            'depenses': depenses,
            'solde': revenus - depenses,
            'nb_transactions': len(monthly_transactions),
            'transactions': monthly_transactions
        }

    def get_category_spending(self, category_name: str, year: int = None, month: int = None) -> float:
        """
        Calcule les dépenses d'une catégorie pour un mois

        Args:
            category_name: Nom de la catégorie
            year: Année (année courante par défaut)
            month: Mois (mois courant par défaut)

        Returns:
            float: Total des dépenses de la catégorie
        """
        now = datetime.now()
        target_year = year or now.year
        target_month = month or now.month

        category_transactions = [
            t for t in self.transactions
            if (t.categorie == category_name and
                t.date.year == target_year and
                t.date.month == target_month and
                t.montant < 0)  # Seulement les dépenses
        ]

        return sum(abs(t.montant) for t in category_transactions)

    def remove_transaction(self, transaction_id: int) -> bool:
        """
        Supprime une transaction

        Args:
            transaction_id: ID de la transaction à supprimer

        Returns:
            bool: True si supprimée avec succès
        """
        for i, transaction in enumerate(self.transactions):
            if transaction.id == transaction_id:
                del self.transactions[i]
                return True
        return False

    def update_transaction(self, transaction_id: int, **kwargs) -> Optional[Transaction]:
        """
        Met à jour une transaction

        Args:
            transaction_id: ID de la transaction
            **kwargs: Champs à mettre à jour

        Returns:
            Transaction: Transaction mise à jour ou None si non trouvée
        """
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                for key, value in kwargs.items():
                    if hasattr(transaction, key):
                        setattr(transaction, key, value)
                return transaction
        return None

    def get_statistics(self) -> Dict[str, Any]:
        """
        Calcule les statistiques complètes

        Returns:
            Dict: Dictionnaire avec toutes les statistiques
        """
        now = datetime.now()
        today = now.date()

        # Transactions du mois courant
        current_month_transactions = [
            t for t in self.transactions
            if t.date.year == now.year and t.date.month == now.month
        ]

        # Revenus et dépenses du mois
        revenus_mois = [t for t in current_month_transactions if t.montant > 0]
        depenses_mois = [t for t in current_month_transactions if t.montant < 0]

        # Statistiques par catégorie
        categories_stats = {}
        for category in self.categories_budgets:
            spent = self.get_category_spending(category.nom)
            remaining = max(0, category.budget_mensuel - spent)
            percentage = (spent / category.budget_mensuel * 100) if category.budget_mensuel > 0 else 0

            status = "good"
            if percentage >= 90:
                status = "over_budget"
            elif percentage >= 70:
                status = "warning"

            categories_stats[category.nom] = {
                'budget': category.budget_mensuel,
                'spent': spent,
                'remaining': remaining,
                'percentage': percentage,
                'status': status,
                'transactions_count': len(self.get_transactions_by_category(category.nom))
            }

        # Top catégories par dépenses
        category_spending = [(cat.nom, self.get_category_spending(cat.nom))
                             for cat in self.categories_budgets]
        top_categories = sorted(
            [(name, amount) for name, amount in category_spending if amount > 0],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            'solde_total': self.get_solde(),
            'revenus_total': self.get_revenus_total(),
            'depenses_total': self.get_depenses_total(),
            'revenus_mois': sum(t.montant for t in revenus_mois),
            'depenses_mois': sum(abs(t.montant) for t in depenses_mois),
            'nombre_transactions': len(self.transactions),
            'nombre_transactions_mois': len(current_month_transactions),
            'nombre_categories': len(self.categories_budgets),
            'categories_actives': len([c for c in self.categories_budgets if c.actif]),
            'categories_stats': categories_stats,
            'top_categories_depenses': top_categories,
            'derniere_transaction': self.transactions[-1].date.isoformat() if self.transactions else None,
            'moyenne_depense_jour': (sum(abs(t.montant) for t in depenses_mois) / today.day) if today.day > 0 else 0,
            'derniere_mise_a_jour': now.isoformat()
        }


    def reset_to_demo_data(self):
        """Remet les données de démonstration"""
        self.clear_all_data()
        self._initialize_demo_data()