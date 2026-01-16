import requests
from typing import List, Dict, Optional

BASE_URL = "http://localhost:8000/api"


class BudgetAPIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    # ========== GET ==========
    def get_operations(self, search: str = None) -> List[Dict]:
        """Récupère toutes les opérations (avec recherche optionnelle)"""
        try:
            params = {}
            if search:
                params["search"] = search
            response = self.session.get(f"{self.base_url}/operations", params=params)
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
    def create_operation(self, date: str, description: str, montant: float, idcompte: int, idtype: int = 1, nomsouscategorie: str = None) -> Dict:
        """Crée une nouvelle opération"""
        try:
            data = {
                "date": date,
                "description": description,
                "montant": montant,
                "idcompte": idcompte,
                "idtype": idtype
            }
            if nomsouscategorie:
                data["nomsouscategorie"] = nomsouscategorie
            response = self.session.post(f"{self.base_url}/operations", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    # ========== PUT ==========
    def update_operation(self, operation_id: int, **kwargs) -> Dict:
        """Met à jour une opération existante"""
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
