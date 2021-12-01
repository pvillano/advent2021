from utils import get_day

lines = get_day(1, 2019).split('\n')

print(sum([int(line)//3-2 for line in lines]))
