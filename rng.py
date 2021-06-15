from typing import List, Union
from numba.experimental import jitclass
from numba import typed, uint8, uint32, boolean, int64, float64

import numpy as np

spec = [
    ('shift', uint32[:]),
#     ('seed', uint32),
#     ('old_seed', uint32),
#     ('verbose', uint8),
#     ('random_numer', uint32[:])
]


class RNG:

    seed: int
    old_seed: int
    shift: uint32[:]
    # verbose: int
    # random_number: List[int]

    def __init__(self, initial_seed: int, shift):
        # if not hasattr(self, "shift"):
        #     raise AttributeError("Base class cannot be instanced directly")

        self.seed: int = np.uint32(initial_seed)
        self.old_seed: int = 0
        # self.verbose: int = verbose
        # self.random_numbers: List[int] = []
        self.shift = shift

        # verbose_str: str = ""
        # if self.verbose > 0:
        #     verbose_str += "New RNG: " + self.__class__.__name__
        # if self.verbose > 1:
        #     verbose_str += " - Start seed: " + str(hex(self.seed))
        # if self.verbose > 3:
        #     verbose_str += " (" + str(self.seed) + ")"
        # if self.verbose > 2:
        #     verbose_str += " " + str(self.shift)
        # if verbose_str:
        #     print(verbose_str)

    def next(self):
        self.old_seed = self.seed
        self.seed ^= np.uint32(self.seed) >> self.shift[0]
        self.seed ^= np.uint32(self.seed) << self.shift[1]
        self.seed ^= np.uint32(self.seed) >> self.shift[2]
        self.seed = np.uint32(self.seed)

        # verbose_str: str = ""
        # if self.verbose > 0:
        #     verbose_str += self.__class__.__name__ + " Next"
        # if self.verbose > 1:
        #     verbose_str += " " + str(hex(self.old_seed)) + " -> " + str(hex(self.seed))
        # if self.verbose > 3:
        #     verbose_str += " (" + str(self.seed) + ")"
        # if self.verbose > 2:
        #     verbose_str += " " + str(self.shift)
        # if verbose_str:
        #     print(verbose_str)

        return self.seed
    
    def previous(self):
        self.old_seed = self.seed
        self.reverse_xor_rshift(self.shift[2])
        self.reverse_xor_lshift(self.shift[1])
        self.reverse_xor_rshift(self.shift[0])
        self.seed = np.uint32(self.seed)

        # verbose_str: str = ""
        # if self.verbose > 0:
        #     verbose_str += self.__class__.__name__ + " Previous"
        # if self.verbose > 1:
        #     verbose_str += " " + str(hex(self.old_seed)) + " -> " + str(hex(self.seed))
        # if self.verbose > 3:
        #     verbose_str += " (" + str(self.seed) + ")"
        # if self.verbose > 2:
        #     verbose_str += " " + str(self.shift)
        # if verbose_str:
        #     print(verbose_str)
        
        return self.seed

    # def gen_random_array(self, amount_of_number: int):
    #     self.random_numbers = [self.seed]
    #
    #     # verbose_str: str = ""
    #     # if self.verbose > 0:
    #     #     verbose_str += (
    #     #         self.__class__.__name__
    #     #         + " Generating "
    #     #         + str(amount_of_number)
    #     #         + " random number"
    #     #     )
    #     # if verbose_str:
    #     #     print(verbose_str)
    #
    #     for i in range(1, amount_of_number):
    #         self.random_numbers.append(
    #             np.uint32(
    #                 i
    #                 + 0x6C078965
    #                 * (
    #                     self.random_numbers[i - 1]
    #                     ^ (self.random_numbers[i - 1] >> 0x1E)
    #                 )
    #             )
    #         )

            # verbose_str: str = ""
            # if self.verbose > 4:
            #     verbose_str += (
            #         "Random Number " + str(i) + ": " + str(hex(self.random_numbers[-1]))
            #     )
            # if self.verbose > 5:
            #     verbose_str += " (" + str(self.random_numbers[-1]) + ")"
            # if verbose_str:
            #     print(verbose_str)

    def revese_random(self, maximum: int = 1):
        random_number: Union[int, float] = 0
        if maximum == 1:
            random_number = self.previous() * 2.3283062e-10
        else:
            random_number = self.previous() % maximum

        # verbose_str: str = ""
        # if self.verbose > 1:
        #     verbose_str += "Generated previous random number: " + str(random_number)
        # if self.verbose > 2:
        #     verbose_str += " (Max: " + str(maximum) + ")"
        # if verbose_str:
        #     print(verbose_str)

        return random_number

    def random(self, maximum: int = 1):
        random_number: Union[int, float] = 0
        if maximum == 1:
            random_number = self.next() * 2.3283062e-10
        else:
            random_number = self.next() % maximum

        # verbose_str: str = ""
        # if self.verbose > 1:
        #     verbose_str += "Generated random number: " + str(random_number)
        # if self.verbose > 2:
        #     verbose_str += " (Max: " + str(maximum) + ")"
        # if verbose_str:
        #     print(verbose_str)

        return random_number

    # def print_seed(self):
    #     print(
    #         "Current Seed: "
    #         + str(hex(self.seed))
    #         + " ("
    #         + str(self.seed)
    #         + ") "
    #         + str(self.shift)
    #     )

    def reverse_xor_lshift(self, shift: int):
        i: int = shift
        while i < 32:
            self.seed ^= np.uint32((self.seed << i) & 0xffffffff)
            i *= 2
        self.seed = np.uint32(self.seed)
        #return np.uint32(self.seed)
    
    def reverse_seed(self):
        num: int = self.seed
        bin_str: np.ndarray = np.zeros(32, dtype=float64)
        i: int = 0
        while i < 32:
            bin_str[i] = num % 2
            num = num // 2
            i += 1
            if num < 1:
                break
        matrix: np.ndarray = 1 << np.arange(bin_str.size, dtype=uint32)
        num = 0
        while i < 32:
            num += matrix[i] * bin_str[i]
        self.seed = np.uint32(num)

    def reverse_xor_rshift(self, shift: uint32):
        self.reverse_seed()
        self.reverse_xor_lshift(shift)
        self.reverse_seed()
        return self.seed
        
        #return self.reverse_bin(self.reverse_xor_lshift(self.reverse_bin(), shift))

@jitclass(spec)
class GameSeeds(RNG):
    """
    This RNG is used to generate the root game seed, and is used to generate other RNG
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x3, 0x17, 0x19])

@jitclass(spec)
class ItemsSeeds(RNG):
    """
    This RNG is used to generate the Pools/ItemsArray seeds
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x1, 0xB, 0x10])

@jitclass(spec)
class PickupSeeds2(RNG):
    """
    This RNG is used to generate the Seed used in the Get Trinket Algorithm
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x1, 0x5, 0x13])

@jitclass(spec)
class CollectiblesSeeds(RNG):
    """
    This RNG is used to generate the Collectibles starting seeds
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x1, 0x13, 0x3])

@jitclass(spec)
class TrinketsSeeds(RNG):
    """
    This RNG is used to generate the Trinkets starting seeds (not the same as the Trinket Pickup Seeds)
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x1, 0x15, 0x14])

@jitclass(spec)
class PillsSeeds(RNG):
    """
    This RNG is used to generate the Pills starting seeds (not the same as the Pills Generation Seeds)
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x1, 0x1B, 0x1B])

@jitclass(spec)
class CardsSeeds(RNG):
    """
    This RNG is used to generate the Cards starting seeds
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x2, 0x5, 0xF])

@jitclass(spec)
class StagesSeeds(RNG):
    """
    This RNG is used to generate the Stage starting seed
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x5, 0x9, 0x7])

@jitclass(spec)
class StatsSeeds(RNG):
    """
    This RNG is used to generate the Stats (Heart, Key, Bombs, Coins and Attributes) of Eden
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x1, 0x5, 0x13])

@jitclass(spec)
class DropSeeds(RNG):
    """
    This RNG is used to calculate most of Eden Drop
    """
    __init__RNG = RNG.__init__
    def __init__(self, initial_seed: int):
        self.__init__RNG(initial_seed, np.array([0x1, 0x5, 0x13], dtype=uint32))

@jitclass(spec)
class CardsDrop(RNG):
    """
    This RNG is used to generate the Cards Drop of Eden
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x3, 0x3, 0x1D])

@jitclass(spec)
class PickupSeeds1(RNG):
    """
    This RNG is used to generate the Pickup and Drop?
    """

    def __init__(self, initial_seed: int, verbose: int):
        super().__init__(initial_seed, verbose, [0x1, 0x9, 0x1D])


@jitclass(spec)
class PillsDrop(RNG):
    """
    This RNG is used to generate the Drop for pills
    """
    __init__RNG = RNG.__init__
    def __init__(self, initial_seed: int, verbose: int):
        self.__init__RNG(initial_seed, [0x2, 0x7, 0x9])
