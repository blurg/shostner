import pytest

from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient

from shostner.main import app

client = TestClient(app)
# Constants

URL = "http://jlugao.com"
ALIAS = "jlugao"

# Scenarios

scenarios("../features/url-shortening.feature")

# Given steps

@given(parsers.parse('That the link with alias "{alias}" and url "{url}" is saved on the database'), target_fixture="context")
def create_link_on_db(alias, url):
    return {}

@when(parsers.parse('I enter the url "{url}"'))
def goto_url(url, context):
    response = client.get(url, allow_redirects=False)
    context["response"] = response
    

@then(parsers.parse('I am redirected to "{url}"'))
def redirected_to_page(url, context):
    response = context["response"]

    assert response.status_code == 307
    assert response.headers["location"] == url

