from unittest.mock import patch
import pytest
import streamlit as st
from tests.unit.conftest import at


def test_app_starts(at):
    """Verify the app starts without errors"""
    assert not at.exception
