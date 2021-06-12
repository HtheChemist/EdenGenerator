from rng import RNG


class PillsInit(RNG):
    shift = [0x1, 0x9, 0x1D]

    def __init__(self, initial_seed: int, verbose: int = 0):
        super().__init__(initial_seed, verbose=verbose)


class PillsSeeds(RNG):
    shift = [0x1, 0x1B, 0x1B]

    def __init__(self, initial_seed: int, verbose: int = 0):
        super().__init__(initial_seed, verbose=verbose)
