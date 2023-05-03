from binc.main import BINC
from binc.map import BINCMap


class BaseBasic:
    base_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                 '8', '9', '+', '/']

    ascii_list = ['NUL', 'SOH', 'STX', 'ETX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 'HT', 'LF', 'VT', 'FF', 'CR', 'SO',
                  'SI', 'DLE', 'DC1', 'DC2', 'DC3', 'DC4', 'NAK', 'SYN', 'ETB', 'CAN', 'EM', 'SUB', 'ESC', 'FS', 'GS',
                  'RS', 'US', ' ', '!', '“', '#', '$', '%', '&', '‘', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1',
                  '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E',
                  'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                  'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'DEL']

    def __init__(self):
        self.binc = BINC()
        self.unknown_char = '�'

    def encode(self, text: str) -> str:
        result = ''
        ascii_bi = ''
        sixes = []

        for char in text:
            ascii_bi += self._get_as_ascii_bi(char)
            if len(ascii_bi) > 23:
                sixes += self._get_group_by_six(ascii_bi[:24])
                ascii_bi = ascii_bi[24:]

        if ascii_bi:
            sixes += (self._get_group_by_six(ascii_bi))

        fours = self._get_group_by_four(sixes)

        # TODO : might to be too long some cases (result)
        for group in fours:
            for part in group:
                if part == '=':
                    result += part
                else:
                    base_dec = self.binc.convert(int(part), _from=BINCMap.BINARY)
                    result += self._get_base_row_by_dec(base_dec)

        return result

    def decode(self, text: str) -> str:
        result = ''
        text_list = list(text)
        group = list()
        bi_group = ""

        for char in text_list:
            if len(group) == 4:
                bi_group += self._group_four_stitch(group)
                group = list()
                group.append(char)
            else:
                group.append(char)

        bi_group += self._group_four_stitch(group)
        eight_group = [bi_group[i:i + 8] for i in range(0, len(bi_group), 8)]

        for each in eight_group:
            dec_each = self.binc.convert(int(each), _from=BINCMap.BINARY)
            result += self._get_ascii_row_by_dec(dec_each)

        return result

    def _get_as_ascii_bi(self, char: str) -> str:
        # TODO : careful with chars not in my list
        ascii_dec = self.ascii_list.index(char)
        ascii_bi = self.binc.convert(ascii_dec, _from=BINCMap.DECIMAL, _to=BINCMap.BINARY)
        char_bi_list = [i for i in str(ascii_bi)]
        return ''.join(['0' for _ in range(8-len(char_bi_list))] + char_bi_list)

    @staticmethod
    def _get_group_by_six(whole: str) -> list:
        result = []
        group = ''

        for char in whole:
            if len(group) == 6:
                result.append(group)
                group = char
            else:
                group += char

        group += (6 - len(group)) * '0'
        result.append(group)

        return result

    def _get_base_row_by_dec(self, row: int):
        return self.base_list[row]

    def _get_ascii_row_by_dec(self, row: int):
        return self.ascii_list[row]

    def _get_base_dec_by_row(self, char: str):
        return self.base_list.index(char)

    def _get_long_base_binary(self, char: str) -> str:
        base_dec = self._get_base_dec_by_row(char)
        binary = str(self.binc.convert(base_dec, _from=BINCMap.DECIMAL, _to=BINCMap.BINARY))
        return "".join(["0" for _ in range(6-len(binary))]) + binary

    @staticmethod
    def _get_group_by_four(lst: list) -> list[list]:
        result = []
        group = []

        for block in lst:
            if len(group) == 4:
                result.append(group)
                group = [block]
            else:
                group.append(block)

        group += ['=' for _ in range(4-len(group))]
        result.append(group)

        return result

    def _group_four_stitch(self, group: list) -> str:
        base_long_bi = ""
        for char in group:
            if char != "=":
                base_long_bi += self._get_long_base_binary(char)
        if "=" in group:
            return base_long_bi[:-group.count("=")*2]
        return base_long_bi
