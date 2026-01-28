from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.orchestrator import BotOrchestrator
from core.detector import BotDetector

app = FastAPI(title="BotHost API")
orchestrator = BotOrchestrator()

class BotAction(BaseModel):
    bot_id: str
    path: str

@app.get("/status")
async def get_status():
    return {"status": "online", "active_bots": len(orchestrator.active_processes)}

@app.post("/bots/start")
async def start_bot(action: BotAction):
    # In a real scenario, we would fetch the command from the detector
    analysis = BotDetector.analyze(action.path)
    if analysis["lang"] == "unknown":
        raise HTTPException(status_code=400, detail="Could not detect bot language.")
    
    # Simple command logic (to be expanded with VENV support)
    cmd = ["python3" if analysis["lang"] == "python" else "node", analysis["entry"]]
    
    success, msg = await orchestrator.start_bot(action.bot_id, cmd, action.path)
    if not success:
        raise HTTPException(status_code=500, detail=msg)
    return {"message": msg}

@app.get("/bots/{bot_id}/logs")
async def get_logs(bot_id: str):
    return {"logs": orchestrator.logs.get(bot_id, [])}
