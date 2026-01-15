# src/models/transaction.py - Modèle Transaction (Port des classes internes C++)
"""
Modèle Transaction - Port exact de la logique C++ vers Python
Conserve toutes les propriétés et méthodes de l'original
"""

from datetime import datetime, date
from typing import Optional, Dict, Any
import json


class Transaction:
    """
    Modèle de transaction - Port exact du C++
    Représente une transaction financière avec toutes ses propriétés
    """

    def __init__(self,
                 montant: float = 0.0,
                 description: str = "",
                 categorie: str = "",
                 date_transaction: Optional[date] = None,
                 type_transaction: str = "depense",  # "depense" ou "revenu"
                 id_transaction: Optional[int] = None,
                 tags: Optional[list] = None,
                 note: str = "",
                 recurrente: bool = False,
                 frequence_recurrence: str = "",
                 date_creation: Optional[datetime] = None):
        """
        Initialise une transaction

        Args:
            montant: Montant de la transaction (positif ou négatif)
            description: Description de la transaction
            categorie: Catégorie de la transaction
            date_transaction: Date de la transaction
            type_transaction: "depense" ou "revenu"
            id_transaction: ID unique de la transaction
            tags: Liste de tags optionnels
            note: Note additionnelle
            recurrente: Si la transaction est récurrente
            frequence_recurrence: Fréquence si récurrente
            date_creation: Date de création de la transaction
        """
        self._montant = float(montant)
        self._description = str(description)
        self._categorie = str(categorie)
        self._date_transaction = date_transaction or date.today()
        self._type_transaction = type_transaction
        self._id_transaction = id_transaction
        self._tags = tags or []
        self._note = str(note)
        self._recurrente = bool(recurrente)
        self._frequence_recurrence = str(frequence_recurrence)
        self._date_creation = date_creation or datetime.now()

        # Propriétés calculées
        self._est_depense = self._type_transaction == "depense"
        self._est_revenu = self._type_transaction == "revenu"

    # ===== PROPRIÉTÉS (équivalent Q_PROPERTY du C++) =====

    @property
    def montant(self) -> float:
        """Montant de la transaction"""
        return self._montant

    @montant.setter
    def montant(self, value: float):
        self._montant = float(value)

    @property
    def description(self) -> str:
        """Description de la transaction"""
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = str(value)

    @property
    def categorie(self) -> str:
        """Catégorie de la transaction"""
        return self._categorie

    @categorie.setter
    def categorie(self, value: str):
        self._categorie = str(value)

    @property
    def date_transaction(self) -> date:
        """Date de la transaction"""
        return self._date_transaction

    @date_transaction.setter
    def date_transaction(self, value: date):
        self._date_transaction = value

    @property
    def type_transaction(self) -> str:
        """Type de transaction : 'depense' ou 'revenu'"""
        return self._type_transaction

    @type_transaction.setter
    def type_transaction(self, value: str):
        if value in ["depense", "revenu"]:
            self._type_transaction = value
            self._est_depense = (value == "depense")
            self._est_revenu = (value == "revenu")

    @property
    def id_transaction(self) -> Optional[int]:
        """ID unique de la transaction"""
        return self._id_transaction

    @id_transaction.setter
    def id_transaction(self, value: int):
        self._id_transaction = value

    @property
    def tags(self) -> list:
        """Liste des tags"""
        return self._tags.copy()

    @tags.setter
    def tags(self, value: list):
        self._tags = list(value) if value else []

    @property
    def note(self) -> str:
        """Note additionnelle"""
        return self._note

    @note.setter
    def note(self, value: str):
        self._note = str(value)

    @property
    def recurrente(self) -> bool:
        """Si la transaction est récurrente"""
        return self._recurrente

    @recurrente.setter
    def recurrente(self, value: bool):
        self._recurrente = bool(value)

    @property
    def frequence_recurrence(self) -> str:
        """Fréquence de récurrence"""
        return self._frequence_recurrence

    @frequence_recurrence.setter
    def frequence_recurrence(self, value: str):
        self._frequence_recurrence = str(value)

    @property
    def date_creation(self) -> datetime:
        """Date de création"""
        return self._date_creation

    # ===== PROPRIÉTÉS CALCULÉES =====

    @property
    def est_depense(self) -> bool:
        """True si c'est une dépense"""
        return self._est_depense

    @property
    def est_revenu(self) -> bool:
        """True si c'est un revenu"""
        return self._est_revenu

    @property
    def montant_affichage(self) -> str:
        """Montant formaté pour affichage avec signe"""
        signe = "+" if self.est_revenu else "-"
        return f"{signe}{abs(self.montant):.2f}€"

    @property
    def montant_absolu(self) -> float:
        """Montant en valeur absolue"""
        return abs(self._montant)

    @property
    def couleur_type(self) -> str:
        """Couleur selon le type (pour UI)"""
        from ui.theme.colors import SUCCESS, ERROR
        return SUCCESS if self.est_revenu else ERROR

    # ===== MÉTHODES =====

    def ajouter_tag(self, tag: str) -> bool:
        """Ajoute un tag s'il n'existe pas déjà"""
        tag = str(tag).strip()
        if tag and tag not in self._tags:
            self._tags.append(tag)
            return True
        return False

    def supprimer_tag(self, tag: str) -> bool:
        """Supprime un tag s'il existe"""
        try:
            self._tags.remove(tag)
            return True
        except ValueError:
            return False

    def has_tag(self, tag: str) -> bool:
        """Vérifie si la transaction a un tag donné"""
        return tag in self._tags

    def est_dans_mois(self, annee: int, mois: int) -> bool:
        """Vérifie si la transaction est dans un mois donné"""
        return (self._date_transaction.year == annee and
                self._date_transaction.month == mois)

    def est_dans_periode(self, date_debut: date, date_fin: date) -> bool:
        """Vérifie si la transaction est dans une période donnée"""
        return date_debut <= self._date_transaction <= date_fin

    def clone(self) -> 'Transaction':
        """Crée une copie de la transaction"""
        return Transaction(
            montant=self.montant,
            description=self.description,
            categorie=self.categorie,
            date_transaction=self.date_transaction,
            type_transaction=self.type_transaction,
            tags=self.tags,
            note=self.note,
            recurrente=self.recurrente,
            frequence_recurrence=self.frequence_recurrence,
            date_creation=self.date_creation
        )

    # ===== SÉRIALISATION JSON (remplace Qt QJsonDocument) =====

    def to_dict(self) -> Dict[str, Any]:
        """Convertit la transaction en dictionnaire pour JSON"""
        return {
            "montant": self._montant,
            "description": self._description,
            "categorie": self._categorie,
            "date_transaction": self._date_transaction.isoformat(),
            "type_transaction": self._type_transaction,
            "id_transaction": self._id_transaction,
            "tags": self._tags,
            "note": self._note,
            "recurrente": self._recurrente,
            "frequence_recurrence": self._frequence_recurrence,
            "date_creation": self._date_creation.isoformat(),
            "version": "2.0"  # Version pour migration future
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Crée une transaction depuis un dictionnaire JSON"""
        try:
            # Parsing des dates
            date_transaction = date.fromisoformat(data.get("date_transaction", date.today().isoformat()))
            date_creation = datetime.fromisoformat(data.get("date_creation", datetime.now().isoformat()))

            return cls(
                montant=float(data.get("montant", 0.0)),
                description=str(data.get("description", "")),
                categorie=str(data.get("categorie", "")),
                date_transaction=date_transaction,
                type_transaction=str(data.get("type_transaction", "depense")),
                id_transaction=data.get("id_transaction"),
                tags=data.get("tags", []),
                note=str(data.get("note", "")),
                recurrente=bool(data.get("recurrente", False)),
                frequence_recurrence=str(data.get("frequence_recurrence", "")),
                date_creation=date_creation
            )
        except (ValueError, KeyError, TypeError) as e:
            raise ValueError(f"Erreur lors de la désérialisation de la transaction: {e}")

    def to_json(self) -> str:
        """Convertit la transaction en JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'Transaction':
        """Crée une transaction depuis JSON"""
        data = json.loads(json_str)
        return cls.from_dict(data)

    # ===== REPRÉSENTATION =====

    def __str__(self) -> str:
        return f"Transaction({self.montant_affichage}, {self.description}, {self.categorie})"

    def __repr__(self) -> str:
        return (f"Transaction(montant={self.montant}, description='{self.description}', "
                f"categorie='{self.categorie}', date={self.date_transaction}, "
                f"type='{self.type_transaction}')")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Transaction):
            return False
        return (self._id_transaction == other._id_transaction and
                self._id_transaction is not None)

    def __hash__(self) -> int:
        return hash(self._id_transaction) if self._id_transaction else hash(id(self))