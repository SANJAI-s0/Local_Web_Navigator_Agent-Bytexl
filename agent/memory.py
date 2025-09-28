# agent/memory.py
"""
SQLite-backed task memory for the Local Web Agent.
"""

import sqlite3
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import os

DEFAULT_DB = "agent_memory.db"

class Memory:
    def __init__(self, db_path: str = DEFAULT_DB):
        self.db_path = db_path
        self._ensure_db()

    def _connect(self):
        return sqlite3.connect(self.db_path, timeout=30, detect_types=sqlite3.PARSE_DECLTYPES)

    def _ensure_db(self):
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks(
                task_id TEXT PRIMARY KEY,
                instruction TEXT,
                result_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at DESC)")
        conn.commit()
        conn.close()

    def save_task(self, task_id: str, instruction: str, result: Dict[str, Any]):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO tasks(task_id, instruction, result_json, created_at) VALUES (?, ?, ?, ?)",
            (task_id, instruction, json.dumps(result, ensure_ascii=False), datetime.utcnow()),
        )
        conn.commit()
        conn.close()

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT task_id, instruction, result_json, created_at FROM tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                "task_id": row[0],
                "instruction": row[1],
                "result": json.loads(row[2]),
                "created_at": str(row[3])
            }
        return None

    def list_tasks(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT task_id, instruction, created_at FROM tasks ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset))
        rows = cur.fetchall()
        conn.close()
        return [{"task_id": r[0], "instruction": r[1], "created_at": str(r[2])} for r in rows]

    def search_tasks(self, q: str, limit: int = 50) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()
        pattern = f"%{q}%"
        cur.execute("SELECT task_id, instruction, created_at FROM tasks WHERE instruction LIKE ? OR result_json LIKE ? ORDER BY created_at DESC LIMIT ?", (pattern, pattern, limit))
        rows = cur.fetchall()
        conn.close()
        return [{"task_id": r[0], "instruction": r[1], "created_at": str(r[2])} for r in rows]

    def delete_task(self, task_id: str) -> bool:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
        affected = cur.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    def export_all(self, path: str):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT task_id, instruction, result_json, created_at FROM tasks ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        data = []
        for r in rows:
            data.append({
                "task_id": r[0],
                "instruction": r[1],
                "result": json.loads(r[2]),
                "created_at": str(r[3])
            })
        with open(path, "w", encoding="utf-8") as f:
            import json as _json
            _json.dump(data, f, ensure_ascii=False, indent=2)
