from dataclasses import dataclass, field
from typing import Dict

@dataclass
class PrismaCounts:
    """Track record counts for the PRISMA flow diagram."""
    identified: int = 0
    duplicates_removed: int = 0
    screened: int = 0
    excluded: int = 0
    full_texts_assessed: int = 0
    full_texts_excluded: int = 0
    included: int = 0

    def to_dict(self) -> Dict[str, int]:
        return {
            "identified": self.identified,
            "duplicates_removed": self.duplicates_removed,
            "screened": self.screened,
            "excluded": self.excluded,
            "full_texts_assessed": self.full_texts_assessed,
            "full_texts_excluded": self.full_texts_excluded,
            "included": self.included,
        }


import matplotlib.pyplot as plt


def export_flow_diagram(counts: PrismaCounts, path: str) -> None:
    """Generate a simple PRISMA flow diagram and save it to a file."""
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis('off')
    text_props = dict(ha='center', va='center', fontsize=10)

    ax.text(0.5, 0.9, f"Records identified: {counts.identified}", **text_props)
    ax.text(0.5, 0.8, f"Duplicates removed: {counts.duplicates_removed}", **text_props)
    ax.text(0.5, 0.7, f"Records screened: {counts.screened}", **text_props)
    ax.text(0.5, 0.6, f"Records excluded: {counts.excluded}", **text_props)
    ax.text(0.5, 0.5, f"Full-texts assessed: {counts.full_texts_assessed}", **text_props)
    ax.text(0.5, 0.4, f"Full-texts excluded: {counts.full_texts_excluded}", **text_props)
    ax.text(0.5, 0.3, f"Studies included: {counts.included}", **text_props)

    plt.savefig(path, bbox_inches='tight')
    plt.close(fig)
