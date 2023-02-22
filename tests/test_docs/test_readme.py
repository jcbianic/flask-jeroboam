"""Testing Examples from README.md file."""
from docs_src.readme.readme00 import app as app00
from docs_src.readme.readme01 import app as app01


def test_readme_00(app=app00):
    """Test the first code snippet from the README.md file."""
    client = app.test_client()
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.data == b"pong"


def test_readme_01(app=app01):
    """Test the second code snippet from the README.md file."""
    client = app.test_client()
    response = client.get("/wines?page=1&perPage=2&search=Champagne")
    assert response.status_code == 200
    assert response.json == [
        {"cuvee": "Brut - Blanc de Blancs", "appellation": "Champagne"},
        {"cuvee": "Grande Cuvée - 170ème Edition", "appellation": "Champagne"},
    ]
