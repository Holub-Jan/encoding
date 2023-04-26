class RomeNums:
    def __init__(self):
        self.order = ('I', 'V', 'X', 'L', 'C', 'D', 'M')
        self.num_map = (1, 5, 10, 50, 100, 500, 1000)

    def encode(self, inpt: int) -> str:
        result = ''
        digits = [int(d) for d in str(inpt)]

        for pos, num in enumerate(digits):
            if num:
                result += self._digit_pairing(num, len(digits) - pos - 1)
        return result

    def decode(self, inpt: str) -> int:
        result = 0
        pointer = self.order[0]
        inpt_lst = list(str(inpt))
        inpt_lst.reverse()

        for digit in inpt_lst:
            d_index = self.order.index(digit)
            if pointer != digit:
                p_index = self.order.index(pointer)
                if d_index > p_index:
                    result += self.num_map[d_index]
                    pointer = self.order[d_index]
                else:
                    result -= self.num_map[d_index]
            else:
                result += self.num_map[d_index]
        return result

    def _digit_pairing(self, num, digit) -> str:
        lst = self._get_dig_list(digit)
        if len(lst) == 3:
            if num < 4:
                numeral = lst[0] * num
            elif num == 4:
                numeral = lst[0] + lst[1]
            elif 4 < num < 9:
                numeral = lst[1] + ((num - 5) * lst[0])
            else:
                numeral = lst[0] + lst[2]
        else:
            numeral = num * lst[0]
        return numeral

    def _get_dig_list(self, digit) -> tuple:
        try:
            lst = self.order[digit * 2: (digit * 2) + 3]
        except IndexError:
            # 'Number is too large for accurate translation!'
            lst = self.order[digit * 2:]
        except Exception as e:
            print(ExceptionGroup, e)
            exit(0)

        return lst
