import json
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path


class ScoreStorage:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "score_data"
    DB_PATH = DATA_DIR / "scores.sqlite3"
    JSON_PATH = DATA_DIR / "scores.json"

    @classmethod
    def save(cls, score, game_mode, level_name, player_name="Jogador"):
        score = int(score)

        if score < 0:
            raise ValueError("A pontuacao nao pode ser negativa")

        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

        created_at = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )

        with closing(sqlite3.connect(cls.DB_PATH)) as conn:
            with conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_name TEXT NOT NULL,
                        score INTEGER NOT NULL,
                        game_mode TEXT NOT NULL,
                        level_name TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                """)

                cursor = conn.execute(
                    """
                    INSERT INTO scores
                    (player_name, score, game_mode, level_name, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        str(player_name),
                        score,
                        str(game_mode),
                        str(level_name),
                        created_at
                    )
                )

                score_id = cursor.lastrowid

        cls.export_json()

        return score_id

    @classmethod
    def all_scores(cls):
        if not cls.DB_PATH.exists():
            return []

        with closing(sqlite3.connect(cls.DB_PATH)) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(
                "SELECT * FROM scores ORDER BY id"
            ).fetchall()

        return [dict(row) for row in rows]

    @classmethod
    def best_scores(cls, limit=10):
        scores = cls.all_scores()

        return sorted(
            scores,
            key=lambda item: (-item["score"], item["id"])
        )[:limit]

    @classmethod
    def export_json(cls):
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

        temporary = cls.DATA_DIR / "scores.json.tmp"

        temporary.write_text(
            json.dumps(
                cls.all_scores(),
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        temporary.replace(cls.JSON_PATH)