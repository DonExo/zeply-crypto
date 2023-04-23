import pytest
from django.urls import reverse

# from .factories import CryptoAddressFactory
from .models import CryptoAddress


@pytest.fixture(autouse=True)
def create_crypto_addresses():
    # CryptoAddressFactory.create_batch(2, type='BTC')
    # CryptoAddressFactory.create(type='ETH')
    # CryptoAddressFactory.create(type='LTC')

    CryptoAddress.objects.create(type='BTC', address='Generated BTC address 1', id=1)
    CryptoAddress.objects.create(type='ETH', address='Generated ETH address 1', id=2)
    CryptoAddress.objects.create(type='BTC', address='Generated BTC address 2', id=3)
    CryptoAddress.objects.create(type='LTC', address='Generated LTC address 1', id=4)


@pytest.mark.django_db
def test_list_crypto_addresses(client):
    response = client.get(reverse('wallets:crypto_addresses'), {})
    assert response.status_code == 200
    assert len(response.json()) == 4


@pytest.mark.django_db
def test_list_sorted_crypto_addresses(client):
    url = reverse('wallets:crypto_addresses') + "?sort=True"
    response = client.get(url)
    assert response.status_code == 200
    # Assert that there are only 3 cryptocurrency types so far
    assert len(response.json()) == 3
    assert response.json()[0]['type'].lower() == 'btc'
    assert response.json()[1]['type'].lower() == 'eth'
    assert response.json()[2]['type'].lower() == 'ltc'


@pytest.mark.django_db
def test_retrieve_crypto_address(client):
    response = client.get(reverse('wallets:crypto_address_detail', kwargs={'pk': 1}))
    assert response.status_code == 200
    assert response.json()['id'] == 1


@pytest.mark.django_db
def test_create_crypto_address(client):
    response = client.post(reverse('wallets:crypto_address_create'), data={'type': 'BTC'})
    assert response.status_code == 201
    assert response.json()['type'] == 'BTC'
    assert CryptoAddress.objects.all().count() == 5
