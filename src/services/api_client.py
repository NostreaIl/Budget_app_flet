import requests
from typing import List, Dict, Optional

BASE_URL = "http://localhost:8000/api"


class BudgetAPIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    # ========== GET ==========
    def get_operations(self) -> List[Dict]:
        """Récupère toutes les opérations"""
        try:
            response = self.session.get(f"{self.base_url}/operations")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_operation(self, operation_id: int) -> Dict:
        """Récupère une opération par son ID"""
        try:
            response = self.session.get(f"{self.base_url}/operations/{operation_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    # ========== POST ==========
    def create_operation(self, date: str, description: str, montant: float, idcompte: int, idtype: int = 1, idsouscategorie: Optional[int] = None) -> Dict:
        """Crée une opération"""
        try:
            data = {
                "date": date,
                "description": description,
                "montant": montant,
                "idcompte": idcompte,
                "idtype": idtype
            }
            if idsouscategorie:
                data["idsouscategorie"] = idsouscategorie
            response = self.session.post(f"{self.base_url}/operations", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    # ========== PUT ==========
    def update_operation(self, operation_id: int, **kwargs) -> Dict:
        """Modifie une opération"""
        try:
            response = self.session.put(
                f"{self.base_url}/operations/{operation_id}",
                json=kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    # ========== DELETE ==========
    def delete_operation(self, operation_id: int) -> Dict:
        """Supprime une opération"""
        try:
            response = self.session.delete(f"{self.base_url}/operations/{operation_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
