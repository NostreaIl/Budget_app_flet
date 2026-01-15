"""
Point d'entrée pour lancer le backend FastAPI
"""
if __name__ == "__main__":
    import os
    import uvicorn
    from dotenv import load_dotenv
    from src.backend.main import app

    load_dotenv()

    # Reload seulement en mode DEBUG
    DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"

    print("🚀 Démarrage du serveur FastAPI...")
    print(f"🔧 Mode: {'DEBUG' if DEBUG_MODE else 'PRODUCTION'}")
    print("📝 Documentation: http://localhost:8000/docs")
    print("🔗 API: http://localhost:8000")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=DEBUG_MODE  # Auto-reload seulement en mode debug
    )
