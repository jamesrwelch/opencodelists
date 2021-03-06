import datetime

from opencodelists.tests.factories import OrganisationFactory, UserFactory

from ..factories import CodelistFactory, ReferenceFactory, SignOffFactory
from .assertions import (
    assert_get_unauthenticated,
    assert_get_unauthorised,
    assert_post_unauthenticated,
    assert_post_unauthorised,
)


def test_get_unauthenticated(client):
    codelist = CodelistFactory()
    assert_get_unauthenticated(client, codelist.get_update_url())


def test_post_unauthenticated(client):
    codelist = CodelistFactory()
    assert_post_unauthenticated(client, codelist.get_update_url())


def test_get_unauthorised(client):
    codelist = CodelistFactory()
    assert_get_unauthorised(client, codelist.get_update_url())


def test_post_unauthorised(client):
    codelist = CodelistFactory()
    assert_post_unauthorised(client, codelist.get_update_url())


def test_get_success(client):
    codelist = CodelistFactory()
    SignOffFactory(codelist=codelist)
    SignOffFactory(codelist=codelist)
    ReferenceFactory(codelist=codelist)
    ReferenceFactory(codelist=codelist)

    client.force_login(codelist.organisation.regular_user)
    response = client.get(codelist.get_update_url())

    assert response.status_code == 200

    form = response.context_data["codelist_form"]
    assert form.data["name"] == codelist.name
    assert form.data["coding_system_id"] == codelist.coding_system_id
    assert form.data["description"] == codelist.description
    assert form.data["methodology"] == codelist.methodology


def test_post_success(client):
    codelist = CodelistFactory()
    signoff_1 = SignOffFactory(codelist=codelist)
    signoff_2 = SignOffFactory(codelist=codelist)
    reference_1 = ReferenceFactory(codelist=codelist)
    reference_2 = ReferenceFactory(codelist=codelist)

    assert codelist.references.count() == 2
    assert codelist.signoffs.count() == 2

    new_signoff_user = UserFactory()

    data = {
        "name": "Test Codelist",
        "coding_system_id": "snomedct",
        "description": "This is a test CHANGED",
        "methodology": "This is how we did it",
        "reference-TOTAL_FORMS": "3",
        "reference-INITIAL_FORMS": "2",
        "reference-MIN_NUM_FORMS": "0",
        "reference-MAX_NUM_FORMS": "1000",
        "reference-0-text": reference_1.text,
        "reference-0-url": reference_1.url,
        "reference-0-id": reference_1.id,
        "reference-0-DELETE": "on",
        "reference-1-text": reference_2.text + " CHANGED",
        "reference-1-url": reference_2.url,
        "reference-1-id": reference_2.id,
        "reference-2-text": "This is a new reference",
        "reference-2-url": "http://example.com",
        "signoff-TOTAL_FORMS": "3",
        "signoff-INITIAL_FORMS": "2",
        "signoff-MIN_NUM_FORMS": "0",
        "signoff-MAX_NUM_FORMS": "1000",
        "signoff-0-user": signoff_1.user.username,
        "signoff-0-date": signoff_1.date,
        "signoff-0-id": signoff_1.id,
        "signoff-0-DELETE": "on",
        "signoff-1-user": signoff_2.user.username,
        "signoff-1-date": signoff_2.date + datetime.timedelta(days=2),
        "signoff-1-id": signoff_2.id,
        "signoff-2-user": new_signoff_user.username,
        "signoff-2-date": "2000-01-01",
    }

    client.force_login(codelist.organisation.regular_user)
    response = client.post(codelist.get_update_url(), data=data)

    assert response.status_code == 302
    assert response.url == f"/codelist/{codelist.organisation.slug}/{codelist.slug}/"

    # we should have still have 2 references but the first should be changed
    # while the second is new.
    assert codelist.references.count() == 2
    assert codelist.references.first().text == reference_2.text + " CHANGED"
    assert codelist.references.last().text == "This is a new reference"

    # we should have still have 2 signoffs but the first should be changed
    # while the second is new.
    assert codelist.signoffs.count() == 2
    assert codelist.signoffs.first().date == signoff_2.date + datetime.timedelta(days=2)
    assert codelist.signoffs.last().user == new_signoff_user


def test_post_invalid(client):
    codelist = CodelistFactory()
    signoff_1 = SignOffFactory(codelist=codelist)
    reference_1 = ReferenceFactory(codelist=codelist)

    # missing signoff-0-date
    data = {
        "name": "Test Codelist",
        "coding_system_id": "snomedct",
        "description": "This is a test",
        "methodology": "This is how we did it",
        "reference-TOTAL_FORMS": "1",
        "reference-INITIAL_FORMS": "0",
        "reference-MIN_NUM_FORMS": "0",
        "reference-MAX_NUM_FORMS": "1000",
        "reference-0-text": reference_1.text,
        "reference-0-url": reference_1.url,
        "signoff-TOTAL_FORMS": "1",
        "signoff-INITIAL_FORMS": "0",
        "signoff-MIN_NUM_FORMS": "0",
        "signoff-MAX_NUM_FORMS": "1000",
        "signoff-0-user": signoff_1.user.username,
    }

    client.force_login(codelist.organisation.regular_user)
    response = client.post(codelist.get_update_url(), data=data)

    # we're returning an HTML response when there are errors so check we don't
    # receive a redirect code
    assert response.status_code == 200

    # confirm we have errors from the signoff formset
    assert response.context_data["signoff_formset"].errors


def test_post_with_duplicate_name(client):
    organisation = OrganisationFactory()

    CodelistFactory(name="Existing Codelist", owner=organisation)
    codelist = CodelistFactory(owner=organisation)

    data = {
        "name": "Existing Codelist",
        "coding_system_id": "snomedct",
        "description": "This is a test CHANGED",
        "methodology": "This is how we did it",
        "reference-TOTAL_FORMS": "0",
        "reference-INITIAL_FORMS": "0",
        "reference-MIN_NUM_FORMS": "0",
        "reference-MAX_NUM_FORMS": "1000",
        "signoff-TOTAL_FORMS": "0",
        "signoff-INITIAL_FORMS": "0",
        "signoff-MIN_NUM_FORMS": "0",
        "signoff-MAX_NUM_FORMS": "1000",
    }

    client.force_login(codelist.organisation.regular_user)
    response = client.post(codelist.get_update_url(), data=data)

    assert response.status_code == 200

    # confirm we have errors from the codelist form
    assert response.context_data["codelist_form"].errors == {
        "__all__": ["There is already a codelist called Existing Codelist"]
    }
