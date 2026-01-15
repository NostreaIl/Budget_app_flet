# src/models/category.py - Modèle CategoryBudget (Port des classes internes C++)
"""
Modèle CategoryBudget - Port exact de la logique C++ vers Python
Gère les catégories avec budgets et limites de dépenses
"""

from typing import Dict, Any, Optional
import json


class CategoryBudget:
    """
    Modèle de catégorie avec budget - Port exact du C++
    Représente une catégorie avec son budget, ses dépenses et sa configuration
    """

    def __init__(self,
                 name: str = "",
                 budget: float = 0.0,
                 spent: float = 0.0,
                 icon: str = "💰",
                 color: str = "#00E5FF",
                 description: str = "",
                 actif: bool = True,
                 budget_mensuel: bool = True,
                 alerte_seuil: float = 0.8,  # Alerte à 80% du budget
                 limite_stricte: bool = False):
        """
        Initialise une catégorie avec budget

        Args:
            name: Nom de la catégorie
            budget: Budget alloué à cette catégorie
            spent: Montant déjà dépensé dans cette catégorie
            icon: Icône (emoji) représentant la catégorie
            color: Couleur hexadécimale de la catégorie
            description: Description de la catégorie
            actif: Si la catégorie est active
            budget_mensuel: Si le budget se remet à zéro chaque mois
            alerte_seuil: Seuil d'alerte (0.0 à 1.0)
            limite_stricte: Si le budget est une limite stricte
        """
        self._name = str(name)
        self._budget = float(budget)
        self._spent = float(spent)
        self._icon = str(icon)
        self._color = str(color)
        self._description = str(description)
        self._actif = bool(actif)
        self._budget_mensuel = bool(budget_mensuel)
        self._alerte_seuil = max(0.0, min(1.0, float(alerte_seuil)))
        self._limite_stricte = bool(limite_stricte)

        # Validation de la couleur
        if not self._color.startswith('#'):
            self._color = "#00E5FF"  # Couleur par défaut

    # ===== PROPRIÉTÉS (équivalent Q_PROPERTY du C++) =====

    @property
    def name(self) -> str:
        """Nom de la catégorie"""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = str(value)

    @property
    def budget(self) -> float:
        """Budget alloué"""
        return self._budget

    @budget.setter
    def budget(self, value: float):
        old_budget = self._budget
        self._budget = max(0.0, float(value))
        # Émettre signal budgetChanged (sera géré par le manager)

    @property
    def spent(self) -> float:
        """Montant dépensé"""
        return self._spent

    @spent.setter
    def spent(self, value: float):
        old_spent = self._spent
        self._spent = max(0.0, float(value))
        # Émettre signal spentChanged (sera géré par le manager)

    @property
    def icon(self) -> str:
        """Icône de la catégorie"""
        return self._icon

    @icon.setter
    def icon(self, value: str):
        self._icon = str(value) if value else "💰"

    @property
    def color(self) -> str:
        """Couleur de la catégorie"""
        return self._color

    @color.setter
    def color(self, value: str):
        if isinstance(value, str) and value.startswith('#'):
            self._color = value
        else:
            self._color = "#00E5FF"

    @property
    def description(self) -> str:
        """Description de la catégorie"""
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = str(value)

    @property
    def actif(self) -> bool:
        """Si la catégorie est active"""
        return self._actif

    @actif.setter
    def actif(self, value: bool):
        self._actif = bool(value)

    @property
    def budget_mensuel(self) -> bool:
        """Si le budget se remet à zéro chaque mois"""
        return self._budget_mensuel

    @budget_mensuel.setter
    def budget_mensuel(self, value: bool):
        self._budget_mensuel = bool(value)

    @property
    def alerte_seuil(self) -> float:
        """Seuil d'alerte (0.0 à 1.0)"""
        return self._alerte_seuil

    @alerte_seuil.setter
    def alerte_seuil(self, value: float):
        self._alerte_seuil = max(0.0, min(1.0, float(value)))

    @property
    def limite_stricte(self) -> bool:
        """Si le budget est une limite stricte"""
        return self._limite_stricte

    @limite_stricte.setter
    def limite_stricte(self, value: bool):
        self._limite_stricte = bool(value)

    # ===== PROPRIÉTÉS CALCULÉES (équivalent aux getters C++) =====

    @property
    def remaining(self) -> float:
        """Montant restant dans le budget"""
        return max(0.0, self._budget - self._spent)

    @property
    def percentage_used(self) -> float:
        """Pourcentage du budget utilisé (0.0 à 100.0+)"""
        if self._budget <= 0:
            return 0.0
        return (self._spent / self._budget) * 100.0

    @property
    def is_over_budget(self) -> bool:
        """True si le budget est dépassé"""
        return self._spent > self._budget and self._budget > 0

    @property
    def is_near_limit(self) -> bool:
        """True si proche de la limite (selon alerte_seuil)"""
        if self._budget <= 0:
            return False
        return (self._spent / self._budget) >= self._alerte_seuil

    @property
    def status(self) -> str:
        """Statut de la catégorie : 'ok', 'warning', 'over'"""
        if not self._actif:
            return 'inactive'
        elif self.is_over_budget:
            return 'over'
        elif self.is_near_limit:
            return 'warning'
        else:
            return 'ok'

    @property
    def status_color(self) -> str:
        """Couleur selon le statut"""
        from src.frontend.theme.colors import COLORS

        status_colors = {
            'ok': COLORS.SUCCESS_REVENUS,
            'warning': COLORS.AVERTISSEMENT,
            'over': COLORS.ERREUR_DEPENSES,
            'inactive': COLORS.TEXTE_SECONDAIRE
        }
        return status_colors.get(self.status, COLORS.SUCCESS_REVENUS)

    @property
    def budget_display(self) -> str:
        """Budget formaté pour affichage"""
        return f"{self._budget:.2f}€"

    @property
    def spent_display(self) -> str:
        """Dépenses formatées pour affichage"""
        return f"{self._spent:.2f}€"

    @property
    def remaining_display(self) -> str:
        """Montant restant formaté pour affichage"""
        return f"{self.remaining:.2f}€"

    @property
    def progress_bar_value(self) -> float:
        """Valeur pour barre de progression (0.0 à 1.0)"""
        if self._budget <= 0:
            return 0.0
        return min(1.0, self._spent / self._budget)

    # ===== MÉTHODES DE GESTION =====

    def add_spending(self, amount: float) -> bool:
        """
        Ajoute une dépense à la catégorie

        Args:
            amount: Montant à ajouter

        Returns:
            bool: True si ajouté, False si limite stricte atteinte
        """
        if amount <= 0:
            return False

        # Vérifier la limite stricte
        if self._limite_stricte and (self._spent + amount) > self._budget:
            return False

        self._spent += amount
        return True

    def remove_spending(self, amount: float) -> bool:
        """
        Retire une dépense de la catégorie

        Args:
            amount: Montant à retirer

        Returns:
            bool: True si retiré avec succès
        """
        if amount <= 0:
            return False

        self._spent = max(0.0, self._spent - amount)
        return True

    def reset_spent(self) -> None:
        """Remet les dépenses à zéro (pour budget mensuel)"""
        self._spent = 0.0

    def can_spend(self, amount: float) -> bool:
        """
        Vérifie si on peut dépenser un montant donné

        Args:
            amount: Montant à vérifier

        Returns:
            bool: True si possible selon les règles de la catégorie
        """
        if not self._actif:
            return False

        if self._limite_stricte:
            return (self._spent + amount) <= self._budget

        return True  # Pas de limite stricte

    def get_overspend_amount(self) -> float:
        """Retourne le montant de dépassement (0 si pas de dépassement)"""
        if self._budget <= 0:
            return 0.0
        return max(0.0, self._spent - self._budget)

    def update_budget_from_spending(self, factor: float = 1.2) -> None:
        """
        Met à jour le budget basé sur les dépenses actuelles

        Args:
            factor: Facteur multiplicateur (par défaut 120% des dépenses)
        """
        if self._spent > 0:
            self._budget = self._spent * factor

    # ===== MÉTHODES DE COMPARAISON =====

    def is_similar_to(self, other_category: 'CategoryBudget') -> bool:
        """Vérifie si deux catégories sont similaires (même nom)"""
        return (isinstance(other_category, CategoryBudget) and
                self._name.lower() == other_category._name.lower())

    def merge_with(self, other_category: 'CategoryBudget') -> None:
        """
        Fusionne avec une autre catégorie (additionne budgets et dépenses)

        Args:
            other_category: Catégorie à fusionner
        """
        if not isinstance(other_category, CategoryBudget):
            return

        self._budget += other_category._budget
        self._spent += other_category._spent

        # Prendre la description la plus longue
        if len(other_category._description) > len(self._description):
            self._description = other_category._description

    # ===== SÉRIALISATION JSON (remplace Qt QJsonDocument) =====

    def to_dict(self) -> Dict[str, Any]:
        """Convertit la catégorie en dictionnaire pour JSON"""
        return {
            "name": self._name,
            "budget": self._budget,
            "spent": self._spent,
            "icon": self._icon,
            "color": self._color,
            "description": self._description,
            "actif": self._actif,
            "budget_mensuel": self._budget_mensuel,
            "alerte_seuil": self._alerte_seuil,
            "limite_stricte": self._limite_stricte,
            "version": "2.0"  # Version pour migration future
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CategoryBudget':
        """Crée une catégorie depuis un dictionnaire JSON"""
        try:
            return cls(
                name=str(data.get("name", "")),
                budget=float(data.get("budget", 0.0)),
                spent=float(data.get("spent", 0.0)),
                icon=str(data.get("icon", "💰")),
                color=str(data.get("color", "#00E5FF")),
                description=str(data.get("description", "")),
                actif=bool(data.get("actif", True)),
                budget_mensuel=bool(data.get("budget_mensuel", True)),
                alerte_seuil=float(data.get("alerte_seuil", 0.8)),
                limite_stricte=bool(data.get("limite_stricte", False))
            )
        except (ValueError, KeyError, TypeError) as e:
            raise ValueError(f"Erreur lors de la désérialisation de la catégorie: {e}")

    def to_json(self) -> str:
        """Convertit la catégorie en JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'CategoryBudget':
        """Crée une catégorie depuis JSON"""
        data = json.loads(json_str)
        return cls.from_dict(data)

    # ===== CATÉGORIES PRÉDÉFINIES =====

    @classmethod
    def create_default_categories(cls) -> list['CategoryBudget']:
        """Crée une liste de catégories par défaut optimisées pour les développeurs Nature & Tech"""
        from src.frontend.theme.colors import COLORS

        return [
            # Catégories développement et tech
            cls(
                name="🖥️ Tech & Développement",
                budget=300.0,
                icon="🖥️",
                color=COLORS.ACCENT_PRINCIPAL,
                description="Matériel informatique, logiciels, formations, abonnements dev"
            ),
            cls(
                name="🔧 Électronique & Composants",
                budget=150.0,
                icon="🔧",
                color=COLORS.ACCENT_SECONDAIRE,
                description="Composants électroniques, Arduino, Raspberry Pi, outils"
            ),
            cls(
                name="🌱 Plantes & Jardinage",
                budget=100.0,
                icon="🌱",
                color=COLORS.SUCCESS_REVENUS,
                description="Plantes d'intérieur, pots, terre, engrais, outils jardinage"
            ),

            # Catégories vie courante
            cls(
                name="🏠 Logement",
                budget=800.0,
                icon="🏠",
                color="#7E57C2",
                description="Loyer, charges, assurance habitation, entretien"
            ),
            cls(
                name="🍕 Alimentation",
                budget=400.0,
                icon="🍕",
                color="#FF7043",
                description="Courses, restaurants, livraisons"
            ),
            cls(
                name="🚗 Transport",
                budget=200.0,
                icon="🚗",
                color="#42A5F5",
                description="Essence, transports en commun, maintenance véhicule"
            ),
            cls(
                name="🎮 Loisirs",
                budget=150.0,
                icon="🎮",
                color="#AB47BC",
                description="Jeux, sorties, abonnements streaming, livres"
            ),
            cls(
                name="🏥 Santé",
                budget=100.0,
                icon="🏥",
                color=COLORS.ERREUR_DEPENSES,
                description="Médecins, pharmacie, mutuelle, sport"
            ),
            cls(
                name="💼 Professionnel",
                budget=200.0,
                icon="💼",
                color="#5D4037",
                description="Formations, certifications, networking, matériel pro"
            ),
            cls(
                name="💰 Épargne & Investissement",
                budget=500.0,
                icon="💰",
                color=COLORS.AVERTISSEMENT,
                description="Épargne mensuelle, investissements, retraite"
            )
        ]

    # ===== REPRÉSENTATION =====

    def __str__(self) -> str:
        status_emoji = {
            'ok': '✅',
            'warning': '⚠️',
            'over': '❌',
            'inactive': '⭕'
        }
        emoji = status_emoji.get(self.status, '❓')
        return f"{emoji} {self._icon} {self._name}: {self.spent_display}/{self.budget_display}"

    def __repr__(self) -> str:
        return (f"CategoryBudget(name='{self._name}', budget={self._budget}, "
                f"spent={self._spent}, status='{self.status}')")

    def __eq__(self, other) -> bool:
        if not isinstance(other, CategoryBudget):
            return False
        return self._name.lower() == other._name.lower()

    def __hash__(self) -> int:
        return hash(self._name.lower())

    def __lt__(self, other) -> bool:
        """Pour le tri par nom"""
        if not isinstance(other, CategoryBudget):
            return NotImplemented
        return self._name.lower() < other._name.lower()