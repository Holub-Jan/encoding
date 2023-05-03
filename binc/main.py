from binc.map import BINCMap


class BINC:
    def convert(self, number: int, _from: int, _to: int = BINCMap.DECIMAL) -> int:
        if number < 0:
            raise ValueError('ValueError: Input in correct type, but cannot be lower then zero.')
        # TODO : can be in that catcher thing I learned at work, to be reworked
        if _from == _to or number == 0:
            return number
        elif _to == BINCMap.DECIMAL:
            return self._to_decimal(number, _from)
        elif _from == BINCMap.DECIMAL:
            return self._from_decimal(number, _to)

        return self._from_decimal(self._to_decimal(number, _from), _to)

    @staticmethod
    def _to_decimal(number: int, _from: int) -> int:
        result = 0
        num_list = list(str(number))
        num_list.reverse()

        for index, num in enumerate(num_list):
            result += int(num) * pow(_from, index)
        return result

    @staticmethod
    def _from_decimal(number: int, _to: int) -> int:
        result = []
        whole = -1

        while whole != 0:
            whole = number // _to
            rest = number % _to
            result.append(str(rest))
            number = whole

        result.reverse()
        return int(''.join(result))
