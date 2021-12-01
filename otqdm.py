from math import log, exp
from time import time
from typing import Sized, Iterable

__all__ = ["otqdm"]

UTF = u" " + u''.join(map(chr, range(0x258F, 0x2587, -1)))


def format_interval(t):
    """[H:]MM:SS"""
    if t is None:
        return '??:??'
    mins, s = divmod(int(t), 60)
    h, m = divmod(mins, 60)
    if h:
        return f'{h:d}:{m:02d}:{s:02d}'
    else:
        return f'{m:02d}:{s:02d}'


def otqdm(iterator: Sized and Iterable, min_interval=1, min_iters=1, unit="it/s",
          n_bars=10, percent_time=False, percent_bars=False, len_iterator=None):

    last_print_t = start_time = time()
    last_print_n = 0
    n = 0
    remaining = None
    n_syms = len(UTF) - 1
    if len_iterator is None:
        try:
            len_iterator = len(iterator)
        except TypeError:
            pass


    for obj in iterator:
        yield obj
        n += 1
        if n - last_print_n >= min_iters:
            delta_t = time() - last_print_t
            if delta_t >= min_interval:
                now = time()
                elapsed = now - start_time
                elapsed_str = format_interval(elapsed)
                rate = n / elapsed if elapsed > 0 else 0

                elapsed_prev = last_print_t - start_time

                if last_print_n and elapsed_prev:
                    exponent = log(elapsed / elapsed_prev) / log(n / last_print_n)
                    if 0.05 <= exponent < 9.95:
                        k = elapsed / (n ** exponent)
                        big_o_str = f"O(n^{exponent:3.1f})"
                        if len_iterator is not None:
                            remaining = k * (len_iterator ** exponent) - elapsed
                    else:
                        base = exp(log(elapsed / elapsed_prev) / (n - last_print_n))
                        if 0.05 <= base < 9.95:
                            k = elapsed / (base ** n)
                            big_o_str = f'O({base:3.1f}^n)'
                            if len_iterator is not None:
                                remaining = k * (base ** len_iterator) - elapsed
                        else:
                            big_o_str = "O(?????)"
                            remaining = None
                else:
                    big_o_str = "O(?????)"
                    remaining = None

                remaining_str = format_interval(remaining)

                if len_iterator is not None:
                    if percent_time:
                        if remaining is None:
                            percent = 0
                        else:
                            percent = elapsed / (remaining + elapsed)
                    else:
                        percent = n / len_iterator

                    if percent_bars:
                        if remaining is None:
                            percent_b = 0
                        else:
                            percent_b = elapsed / (remaining + elapsed)
                    else:
                        percent_b = n / len_iterator

                    bar_length, frac_bar_length = divmod(int(percent_b * n_bars * n_syms), n_syms)
                    bar_str = UTF[-1] * bar_length
                    if bar_length < n_bars:  # whitespace padding
                        bar_str = bar_str + UTF[frac_bar_length] + UTF[0] * (n_bars - bar_length - 1)

                    print(f"{big_o_str} {percent * 100:3.0f}%|{bar_str}| {n}/{len_iterator} [{elapsed_str}/{remaining_str}, {rate:5.2f}{unit}]")
                else:
                    print(f"{big_o_str} ??%|??????????| {n}/{'?'*len(str(n))} [{elapsed_str}/{remaining_str}, {rate:5.2f}{unit}]")

                last_print_n = n
                last_print_t = now


if __name__ == '__main__':

    def fibonacci(i):
        if i < 2:
            return 1
        return fibonacci(i - 1) + fibonacci(i - 2)


    print(">>>for i in otdqm(range(40)):\n"
          "...    fibonacci(i)")
    for i in otqdm(range(40)):
        fibonacci(i)
