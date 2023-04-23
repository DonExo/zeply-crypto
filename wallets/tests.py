import pytest
from django.urls import reverse, NoReverseMatch

from .factories import CryptoAddressFactory
from .models import CryptoAddress


@pytest.fixture(autouse=True)
def create_crypto_addresses():
    # Use these 4 addresses as a seed
    CryptoAddressFactory.create_batch(2, type='BTC')
    CryptoAddressFactory.create(type='ETH')
    CryptoAddressFactory.create(type='LTC')


@pytest.mark.django_db
def test_list_crypto_addresses(client):
    response = client.get(reverse('wallets:crypto_addresses'))
    assert response.status_code == 200
    assert len(response.json()) == 4


@pytest.mark.django_db
def test_list_sorted_crypto_addresses(client):
    url = reverse('wallets:crypto_addresses') + "?sort=True"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 3  # Assert that there are only 3 cryptocurrency types so far
    assert response.json()[0]['type'] == 'BTC'
    assert len(response.json()[0]['addresses']) == 2  # 2 Addresses from the seed
    assert response.json()[1]['type'] == 'ETH'
    assert response.json()[2]['type'] == 'LTC'


@pytest.mark.django_db
def test_retrieve_crypto_address_success(client):
    crypto_address = CryptoAddress.objects.first()
    response = client.get(reverse('wallets:crypto_address_detail', kwargs={'id': crypto_address.id}))
    assert response.status_code == 200
    assert response.json()['id'] == crypto_address.id


@pytest.mark.django_db
def test_retrieve_crypto_address_no_id_provided(client):
    with pytest.raises(NoReverseMatch):
        client.get(reverse('wallets:crypto_address_detail', kwargs={}))


@pytest.mark.django_db
def test_retrieve_crypto_address_not_found(client):
    response = client.get(reverse('wallets:crypto_address_detail', kwargs={'id': 999}))
    assert response.json() == {'detail': 'Not found.'}
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_crypto_address(client):
    response = client.post(reverse('wallets:crypto_address_create'), data={'type': 'BTC'})
    assert response.status_code == 201
    assert response.json()['type'] == 'BTC'
    assert CryptoAddress.objects.all().count() == 5


@pytest.mark.django_db
def test_create_crypto_address_non_capitalized_ticker(client):
    response = client.post(reverse('wallets:crypto_address_create'), data={'type': 'lTc'})
    assert response.status_code == 201
    assert response.json()['type'] == 'LTC'
    assert CryptoAddress.objects.all().count() == 5


@pytest.mark.django_db
def test_create_crypto_address_omit_type(client):
    response = client.post(reverse('wallets:crypto_address_create'), data={})
    assert response.status_code == 400
    assert response.json()["type"] == ['This field is required.']


@pytest.mark.django_db
def test_create_crypto_address_invalid_crypto_currency(client):
    response = client.post(reverse('wallets:crypto_address_create'), data={'type': 'foobar'})
    assert response.status_code == 400
    assert response.json()["error"] == 'Invalid cryptocurrency ticker provided.'
