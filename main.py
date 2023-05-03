import string

from base_six_four.main import BaseBasic
from binc.main import BINC
from binc.map import BINCMap


if __name__ == "__main__":
    base = BaseBasic()
    original = 'AB'
    enco_text = base.encode(original)
    deco_text = base.decode(enco_text)
    print(f'Original: {original}\nBase encoded: {enco_text}\nBase decoded: {deco_text}')
