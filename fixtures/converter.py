import codecs
from pathlib import Path

encoded = codecs.open(Path(__file__).parent / 'initial_data.json', 'r', 'utf-8').read().encode(
            'ascii', 'backslashreplace')

with open(Path(__file__).parent / 'initial_data_with_ascii.json', 'w') as f:
    f.write(encoded.decode())