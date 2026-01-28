import os
import subprocess
import pwd
import grp
from pathlib import Path

class BotSecurity:
    """
    Gère la sécurité et l'isolation des processus des bots.
    """

    @staticmethod
    def sanitize_path(path: str) -> bool:
        """
        Vérifie que le chemin du bot reste dans le dossier autorisé 
        et n'essaie pas de remonter dans le système (ex: ../../).
        """
        resolved_path = Path(path).resolve()
        base_runtime = Path("./runtime").resolve()
        return base_runtime in resolved_path.parents or resolved_path == base_runtime

    @staticmethod
    def get_restricted_env() -> dict:
        """
        Retourne un dictionnaire de variables d'environnement limité.
        On supprime les accès aux clés système pour protéger le serveur.
        """
        # On garde le strict minimum nécessaire au fonctionnement de Python/Node
        safe_keys = ['PATH', 'LANG', 'LC_ALL', 'PYTHONPATH']
        return {k: os.environ[k] for k in safe_keys if k in os.environ}

    @staticmethod
    def apply_resource_limits():
        """
        Note: Cette fonction est un emplacement pour les limites système (ulimit).
        Elle sera complétée par le module Rust pour une gestion fine de la RAM.
        """
        pass
