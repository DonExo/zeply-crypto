import pytest
from django.urls import NoReverseMatch, reverse

from freezegun import freeze_time

from .factories import CryptoAddressFactory
from .models import CryptoAddress, CryptoWallet


@pytest.fixture(autouse=True)
def address_and_wallet_seed():
    # Use these 4 addresses as a seed, this will also generate one single CryptoWallet associated with all these
    CryptoAddressFactory.create_batch(2, type="BTC")
    CryptoAddressFactory.create(type="ETH")
    CryptoAddressFactory.create(type="LTC")


@pytest.fixture
def crypto_mnemonic():
    # Yeah, don't try to import this seed, it's a dummy one.
    return "life scale blush moral timber cruise swap crazy worry ice route describe"


@pytest.mark.django_db
def test_list_crypto_addresses(client):
    response = client.get(reverse("wallets:crypto_addresses"))
    assert response.status_code == 200
    assert len(response.json()) == 4


@pytest.mark.django_db
def test_list_sorted_crypto_addresses(client):
    url = reverse("wallets:crypto_addresses") + "?sort=True"
    response = client.get(url)
    assert response.status_code == 200
    assert (
        len(response.json()) == 3
    )  # Assert that there are only 3 cryptocurrency types so far
    assert response.json()[0]["type"] == "BTC"
    assert len(response.json()[0]["addresses"]) == 2  # 2 Addresses from the seed
    assert response.json()[1]["type"] == "ETH"
    assert response.json()[2]["type"] == "LTC"


@pytest.mark.django_db
def test_retrieve_crypto_address_success(client):
    crypto_address = CryptoAddress.objects.first()
    response = client.get(
        reverse("wallets:crypto_address_detail", kwargs={"id": crypto_address.id})
    )
    assert response.status_code == 200
    assert response.json()["id"] == crypto_address.id


@pytest.mark.django_db
def test_retrieve_crypto_address_no_id_provided(client):
    with pytest.raises(NoReverseMatch):
        client.get(reverse("wallets:crypto_address_detail", kwargs={}))


@pytest.mark.django_db
def test_retrieve_crypto_address_not_found(client):
    response = client.get(reverse("wallets:crypto_address_detail", kwargs={"id": 999}))
    assert response.json() == {"detail": "Not found."}
    assert response.status_code == 404


@freeze_time("2022-01-01 01:01:01.0")  # Translates to '1640998861.0' in timestamp
@pytest.mark.django_db
def test_create_crypto_address_bitcoin_success(client, crypto_mnemonic):
    response = client.post(
        reverse("wallets:crypto_address_create"), data={"type": "BTC", "mnemonic": crypto_mnemonic}
    )
    assert response.status_code == 201
    assert response.json()["type"] == "BTC"
    assert CryptoAddress.objects.all().count() == 5
    assert CryptoWallet.objects.all().count() == 2  # This generated a new wallet alongside the address
    assert CryptoWallet.objects.last().wallet_name == "wallet_testnet_1640998861.0"


@freeze_time("2022-01-01 01:01:01.0")  # Translates to '1640998861.0' in timestamp
@pytest.mark.django_db
def test_create_crypto_address_ethereum_success(client):
    response = client.post(
        reverse("wallets:crypto_address_create"), data={"type": "ETH", "mnemonic": crypto_mnemonic}
    )
    assert response.status_code == 201
    assert response.json()["type"] == "ETH"
    assert CryptoAddress.objects.all().count() == 5
    assert CryptoWallet.objects.all().count() == 2  # This generated a new wallet alongside the address
    assert CryptoWallet.objects.last().wallet_name == "wallet_eth_1640998861.0"


@pytest.mark.django_db
def test_create_crypto_address_non_capitalized_ticker(client, crypto_mnemonic):
    response = client.post(
        reverse("wallets:crypto_address_create"), data={"type": "lTc", "mnemonic": crypto_mnemonic}
    )
    assert response.status_code == 201
    assert response.json()["type"] == "LTC"
    assert CryptoAddress.objects.all().count() == 5


@pytest.mark.django_db
def test_create_crypto_address_omit_type(client):
    response = client.post(reverse("wallets:crypto_address_create"), data={})
    assert response.status_code == 400
    assert response.json()["type"] == ["This field is required."]
    assert CryptoWallet.objects.all().count() == 1  # This did not generate new wallet, this is the seeded one


@pytest.mark.django_db
def test_create_crypto_address_invalid_crypto_currency(client):
    response = client.post(
        reverse("wallets:crypto_address_create"), data={"type": "foobar", "mnemonic": crypto_mnemonic}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid cryptocurrency ticker provided."
    assert CryptoWallet.objects.count() == 1  # This did not generate new wallet, this is the seeded one