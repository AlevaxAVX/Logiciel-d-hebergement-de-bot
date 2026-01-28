import uvicorn
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes.bots import router as bots_router

# Création des dossiers nécessaires s'ils n'existent pas
directories = ["runtime", "storage", "web"]
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

app = FastAPI(
    title="BotHost Server",
    description="Logiciel d'hébergement simplifié pour bots Discord"
)

# Inclusion des routes API
app.include_router(bots_router)

# Service des fichiers statiques pour le frontend
# On monte le dossier 'web' pour que l'index.html soit accessible sur /
app.mount("/", StaticFiles(directory="web", html=True), name="frontend")

if __name__ == "__main__":
    print("🚀 BotHost démarre sur http://localhost:8000")
    # Lancement du serveur Web avec Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
