from binc.main import BINC
from binc.map import BINCMap

if __name__ == "__main__":
    cod = BINC()
    nums = [4, 9, 10, 18, 89]
    for num in nums:
        to_six = cod.convert(num, _from=BINCMap.DECIMAL, _to=BINCMap.SIX)
        to_two = cod.convert(to_six, _from=BINCMap.SIX, _to=BINCMap.BINARY)
        to_ten = cod.convert(to_two, _from=BINCMap.BINARY)
        print(f'From ten: {num}, to six: {to_six}, to two: {to_two}, back to ten: {to_ten}')
