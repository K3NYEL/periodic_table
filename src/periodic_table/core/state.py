"""Small JSON-backed user state store, isolated from scientific source data."""
import json
from pathlib import Path
from typing import Any


DEFAULT_STATE: dict[str, Any] = {
    "favorites": [],
    "notes": {},
    "collections": {"Examen viernes": [], "Metales": [], "Gases": []},
    "settings": {
        "Tema": "Claro", "Idioma": "Español", "Temperatura": "K",
        "Tamaño": "Normal", "Colores": True,
    },
    "quiz": {"best_streak": 0},
}


class UserState:
    def __init__(self, path: Path | None = None):
        self.path = path or Path.home() / ".periodic_table" / "state.json"
        self.data = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return json.loads(json.dumps(DEFAULT_STATE))
        try:
            stored = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return json.loads(json.dumps(DEFAULT_STATE))
        state = json.loads(json.dumps(DEFAULT_STATE))
        if isinstance(stored, dict):
            for key in ("favorites", "notes", "collections", "settings", "quiz"):
                if isinstance(stored.get(key), type(state[key])):
                    state[key] = stored[key]
        return state

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(self.path)

    @property
    def favorites(self) -> set[int]:
        return {int(number) for number in self.data["favorites"]}

    def set_favorite(self, number: int, enabled: bool) -> None:
        favorites = self.favorites
        favorites.add(int(number)) if enabled else favorites.discard(int(number))
        self.data["favorites"] = sorted(favorites)
        self.save()

    def set_note(self, number: int, note: str) -> None:
        notes = self.data["notes"]
        if note.strip():
            notes[str(int(number))] = note.strip()
        else:
            notes.pop(str(int(number)), None)
        self.save()

    def set_setting(self, key: str, value: Any) -> None:
        self.data["settings"][key] = value
        self.save()

    def add_collection(self, name: str) -> bool:
        name = name.strip()
        collections = self.data["collections"]
        if not name or name in collections:
            return False
        collections[name] = []
        self.save()
        return True

    def toggle_collection_member(self, name: str, number: int) -> None:
        collections = self.data["collections"]
        if name not in collections:
            return
        members = {int(item) for item in collections[name]}
        members.symmetric_difference_update({int(number)})
        collections[name] = sorted(members)
        self.save()
