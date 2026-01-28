import os
from pathlib import Path

class BotDetector:
    """
    Automatically detects bot language and entry point.
    """
    @staticmethod
    def analyze(directory: str):
        path = Path(directory)
        files = [f.name for f in path.iterdir() if f.is_file()]
        
        # Check for Python
        if "requirements.txt" in files or any(f.endswith(".py") for f in files):
            entry_point = BotDetector._find_entry(files, [ "main.py", "bot.py", "app.py", "index.py"])
            return {"lang": "python", "entry": entry_point}
        
        # Check for Node.js
        if "package.json" in files or any(f.endswith(".js") for f in files):
            entry_point = BotDetector._find_entry(files, ["index.js", "bot.js", "main.js", "app.js"])
            return {"lang": "nodejs", "entry": entry_point}
            
        return {"lang": "unknown", "entry": None}

    @staticmethod
    def _find_entry(files, priorities):
        for p in priorities:
            if p in files:
                return p
        # Fallback to the first found file with correct extension
        for f in files:
            if f.endswith(".py") or f.endswith(".js"):
                return f
        return None
