"""Testing Base Class from Flask-Jeroboam."""
from flask_jeroboam.blueprint import APIBlueprint
from flask_jeroboam.jeroboam import Jeroboam
from flask import Blueprint, Flask


def test_blueprint(
    inbound_model_test_class,
    reponse_model_test_class,
):
    """Test BluePrint Initialisation"""
    blueprint = APIBlueprint("test", __name__)

    assert issubclass(blueprint.__class__, Blueprint)


def test_jeroboam(
    inbound_model_test_class,
    reponse_model_test_class,
):
    """Test Jeroboam Initialisation"""
    app = Jeroboam("test")

    assert issubclass(app.__class__, Flask)
