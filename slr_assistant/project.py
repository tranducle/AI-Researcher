from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import sqlite3
from .prisma import PrismaCounts


@dataclass
class Study:
    title: str
    authors: str
    abstract: str
    doi: Optional[str] = None
    pdf_path: Optional[str] = None
    included: bool = False
    exclusion_reason: Optional[str] = None
    extracted_data: dict = field(default_factory=dict)


class SLRProject:
    """Manage project data and interactions."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self.db = self.path / "project.db"
        self.conn = sqlite3.connect(self.db)
        self._init_db()
        self.prisma = PrismaCounts()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS studies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                authors TEXT,
                abstract TEXT,
                doi TEXT,
                pdf_path TEXT,
                included INTEGER DEFAULT 0,
                exclusion_reason TEXT
            )
            """
        )
        self.conn.commit()

    def add_study(self, study: Study) -> int:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO studies (title, authors, abstract, doi, pdf_path, included, exclusion_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                study.title,
                study.authors,
                study.abstract,
                study.doi,
                study.pdf_path,
                int(study.included),
                study.exclusion_reason,
            ),
        )
        self.conn.commit()
        self.prisma.identified += 1
        return cur.lastrowid

    def list_studies(self, included: Optional[bool] = None) -> List[Study]:
        cur = self.conn.cursor()
        query = "SELECT title, authors, abstract, doi, pdf_path, included, exclusion_reason FROM studies"
        if included is not None:
            query += " WHERE included = ?"
            cur.execute(query, (int(included),))
        else:
            cur.execute(query)
        rows = cur.fetchall()
        studies = [
            Study(
                title=row[0],
                authors=row[1],
                abstract=row[2],
                doi=row[3],
                pdf_path=row[4],
                included=bool(row[5]),
                exclusion_reason=row[6],
            )
            for row in rows
        ]
        return studies

    def update_inclusion(self, study_id: int, included: bool, reason: Optional[str] = None) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE studies SET included = ?, exclusion_reason = ? WHERE id = ?",
            (int(included), reason, study_id),
        )
        self.conn.commit()
        if included:
            self.prisma.included += 1
        else:
            self.prisma.full_texts_excluded += 1

    def close(self) -> None:
        self.conn.close()
