def test_import_blueprint_and_app():
    """GIVEN the flask_jeroboam module
    WHEN I import the blueprint and the app
    THEN I get the blueprint and the app
    """
    from flask_jeroboam import APIBlueprint
    from flask_jeroboam import Jeroboam

    assert APIBlueprint
    assert Jeroboam
