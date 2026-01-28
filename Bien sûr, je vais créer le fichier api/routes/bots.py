from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import uuid
from core.models import BotConfig, BotStatus, BotCreate
from core.orchestrator import BotOrchestrator
from core.detector import BotDetector

# On initialise le routeur et l'orchestrateur (normalement injecté ou global)
router = APIRouter(prefix="/bots", tags=["bots"])
orchestrator = BotOrchestrator()

# Simulons une base de données en mémoire pour cet exemple
# Dans la version finale, cela sera remplacé par des appels SQLite
db_bots: List[BotConfig] = []

@router.get("/", response_model=List[BotConfig])
async def list_bots():
    """
    Récupère la liste de tous les bots configurés.
    """
    return db_bots

@router.post("/create", response_model=BotConfig)
async def create_bot(data: BotCreate):
    """
    Enregistre un nouveau bot après analyse automatique du dossier.
    """
    # Chemin par défaut pour le stockage des bots (à adapter selon l'installation)
    bot_path = f"./runtime/{uuid.uuid4()}"
    
    # Analyse automatique via le détecteur
    analysis = BotDetector.analyze(bot_path)
    
    new_bot = BotConfig(
        id=str(uuid.uuid4()),
        name=data.name,
        path=bot_path,
        language=analysis["lang"],
        entry_point=analysis["entry"] or "main.py"
    )
    
    db_bots.append(new_bot)
    return new_bot

@router.post("/{bot_id}/start")
async def start_bot(bot_id: str):
    """
    Lance le processus d'un bot spécifique.
    """
    bot = next((b for b in db_bots if b.id == bot_id), None)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot introuvable")
    
    # Détermination de la commande de lancement
    cmd = ["python3" if bot.language == "python" else "node", bot.entry_point]
    
    success, message = await orchestrator.start_bot(bot.id, cmd, bot.path)
    if not success:
        raise HTTPException(status_code=500, detail=message)
        
    return {"status": "started", "message": message}

@router.post("/{bot_id}/stop")
async def stop_bot(bot_id: str):
    """
    Arrête le processus d'un bot.
    """
    success, message = await orchestrator.stop_bot(bot_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"status": "stopped", "message": message}

@router.get("/{bot_id}/status", response_model=BotStatus)
async def get_bot_status(bot_id: str):
    """
    Récupère l'état de santé et les statistiques d'un bot.
    """
    is_running = bot_id in orchestrator.active_processes
    return BotStatus(
        bot_id=bot_id,
        is_running=is_running,
        memory_usage=0.0, # À lier avec le futur module Rust/Monitoring
        cpu_usage=0.0
    )
