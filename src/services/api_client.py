import requests
from typing import List, Dict, Optional

BASE_URL = "http://localhost:8000/api"


class BudgetAPIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    # ========== GET ==========
    def get_transactions(self) -> List[Dict]:
        """Récupère transactions"""
        try:
            response = self.session.get(f"{self.base_url}/transactions")
            response.raise_for_status()  # Erreur si 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_transaction(self, tx_id: int) -> Dict:
        """Récupère 1 transaction"""
        try:
            response = self.session.get(f"{self.base_url}/transactions/{tx_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    # ========== POST ==========
    def create_transaction(self, description: str, montant: float, idcompte: int) -> Dict:
        """Crée transaction"""
        try:
            data = {
                "description": description,
                "montant": montant,
                "idcompte": idcompte,
                "idtype": 1  # Default "depense"
            }
            response = self.session.post(f"{self.base_url}/transactions", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    # ========== PUT ==========
    def update_transaction(self, tx_id: int, **kwargs) -> Dict:
        """Modifie transaction"""
        try:
            response = self.session.put(
                f"{self.base_url}/transactions/{tx_id}",
                json=kwargs  # {"description": "...", "montant": -5.0}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    # ========== DELETE ==========
    def delete_transaction(self, tx_id: int) -> Dict:
        """Supprime transaction"""
        try:
            response = self.session.delete(f"{self.base_url}/transactions/{tx_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
