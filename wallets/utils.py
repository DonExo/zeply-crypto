import hashlib


def hash_data(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    return sha256.hexdigest()


def compare_hashed_data(plain_data, hashed_data):
    plain_data_hash = hash_data(plain_data)
    return plain_data_hash == hashed_data
