from pytest import raises, fixture, fail
import bitforge.networks
from bitforge.privkey import PrivateKey
from bitforge.pubkey import PublicKey


data = {
    'privkey_hex': 'd862dc70f3a40b52e9ed3567b073e32dc543f3b51c9eae8f3ac3e95a05af6b65',
    'pubkey_pair': (
        83234559159195082631296919245646869202106616233090297833190812666019583768233L,
        88596170374369955503701867101393570128177433697625675006047409032754219321755L
    ),
    'pubkey_bin' : '\x03\xb8\x05\x17K\xd4\x96\xb2u\xe7\x11\xd5\xa9\xf1\xbc\xba\xa4\xbb\xa1\xa7qv\xdb\xdb_\xdd\x8bv\x9d\xa6*6\xa9',
    'pubkey_hex' : {
        'compressed'  : '03b805174bd496b275e711d5a9f1bcbaa4bba1a77176dbdb5fdd8b769da62a36a9',
        'uncompressed': '04b805174bd496b275e711d5a9f1bcbaa4bba1a77176dbdb5fdd8b769da62a36a9c3dfa7c8ccb509f9a66efd6d8d1db6b25aa7c100476154b6303d76c28eda099b',
    },
    'address': {
        'live_compressed'  : '1N8FRuC7P1ZtLfkjrvGrCTGkZXuLk4p8rE',
        'live_uncompressed': '1MGu43MAwpDnKb4d3xmNZvupLwk6iaaQay',
        'test_compressed'  : 'n2eCixH6C3197nEMaVFE2NV5RXW3cazW4Q',
        'test_uncompressed': 'n1nrM6S9kqf36hYEmXjkPr89CwLobCH2nR',
    }
}


class TestPublicKey:

    def test_invalid_pair(self):
        with raises(PublicKey.InvalidPair):
            PublicKey((0, 0))


    def test_unknown_network(self):
        with raises(PublicKey.UnknownNetwork):
            PublicKey(data['pubkey_pair'], network = 'a')


    def test_from_private_key(self):
        privkey = PrivateKey.from_hex(data['privkey_hex'])
        pubkey  = PublicKey.from_private_key(privkey)

        assert pubkey.network is privkey.network
        assert pubkey.compressed == privkey.compressed
        assert pubkey.pair == data['pubkey_pair']


    def test_from_hex_compressed(self):
        pubkey = PublicKey.from_hex(data['pubkey_hex']['compressed'])

        assert pubkey.pair == data['pubkey_pair']
        assert pubkey.compressed is True
        assert pubkey.network is bitforge.networks.default


    def test_to_hex_compressed(self):
        string = data['pubkey_hex']['compressed']
        assert PublicKey.from_hex(string).to_hex() == string


    def test_from_hex_uncompressed(self):
        pubkey = PublicKey.from_hex(data['pubkey_hex']['uncompressed'])

        assert pubkey.pair == data['pubkey_pair']
        assert pubkey.compressed is False
        assert pubkey.network is bitforge.networks.default


    def test_from_hex_errors(self):
        with raises(PublicKey.InvalidHex): PublicKey.from_hex('a')
        with raises(PublicKey.InvalidHex): PublicKey.from_hex('a@')


    def test_to_hex_uncompressed(self):
        string = data['pubkey_hex']['uncompressed']
        assert PublicKey.from_hex(string).to_hex() == string


    def test_from_bytes(self):
        pubkey = PublicKey.from_bytes(data['pubkey_bin'])

        assert pubkey.pair == data['pubkey_pair']
        assert pubkey.compressed is True
        assert pubkey.network is bitforge.networks.default

        with raises(PublicKey.InvalidBinary):
            PublicKey.from_bytes('a')

        with raises(PublicKey.InvalidBinary):
            PublicKey.from_bytes('a' * 70)


    def test_to_bytes(self):
        bytes = data['pubkey_bin']
        assert PublicKey.from_bytes(bytes).to_bytes() == bytes


    def test_to_address_live_compress(self):
        pubkey = PublicKey.from_hex(data['pubkey_hex']['compressed'], bitforge.networks.livenet)
        assert pubkey.to_address().to_string() == data['address']['live_compressed']


    def test_to_address_live_uncompress(self):
        pubkey = PublicKey.from_hex(data['pubkey_hex']['uncompressed'], bitforge.networks.livenet)
        assert pubkey.to_address().to_string() == data['address']['live_uncompressed']


    def test_to_address_test_compress(self):
        pubkey = PublicKey.from_hex(data['pubkey_hex']['compressed'], bitforge.networks.testnet)
        assert pubkey.to_address().to_string() == data['address']['test_compressed']


    def test_to_address_test_uncompress(self):
        pubkey = PublicKey.from_hex(data['pubkey_hex']['uncompressed'], bitforge.networks.testnet)
        assert pubkey.to_address().to_string() == data['address']['test_uncompressed']
