"""
Point d'entrée pour lancer le backend FastAPI
"""
if __name__ == "__main__":
    import uvicorn
    from src.backend.main import app

    print("🚀 Démarrage du serveur FastAPI...")
    print("📝 Documentation: http://localhost:8000/docs")
    print("🔗 API: http://localhost:8000")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
