"""Fictional CRUD operations."""

from typing import TYPE_CHECKING
from typing import Dict
from typing import List
from typing import Optional


if TYPE_CHECKING:
    from docs_src.readme.readme01 import GenericPagination

wines: List[Dict[str, str]] = [
    {
        "appellation": "Margaux",
        "domain": "Château Magaux",
        "cuvee": "Pavillon Rouge",
        "color": "Rouge",
    },
    {
        "appellation": "Meursault",
        "domain": "Domaine Comte Armand ",
        "cuvee": "Meursault",
        "color": "Blanc",
    },
    {
        "appellation": "Champagne",
        "domain": "Billecart-Salmon",
        "cuvee": "Brut - Blanc de Blancs",
        "color": "Blanc",
    },
    {
        "appellation": "Champagne",
        "domain": "Krug",
        "cuvee": "Grande Cuvée - 170ème Edition",
        "color": "Blanc",
    },
    {
        "appellation": "Champagne",
        "domain": "Maison Taittinger",
        "cuvee": "Grand Cru - Brut - Prélude",
        "color": "Blanc",
    },
]


def get_wines(pagination: "GenericPagination", search: Optional[str]) -> List[dict]:
    """Get wines from a list."""
    if search:
        wines_filtered = [
            wine
            for wine in wines
            if search.lower() in f"{wine['appellation']}-{wine['cuvee']}".lower()
        ]
    else:
        wines_filtered = wines
    return wines_filtered[pagination.offset : pagination.offset + pagination.per_page]
