from typing import List

from rng import RNG, StagesSeeds


class Stage:
    seed: int
    rng: RNG
    verbose: int

    def __init__(self, seed: int, verbose: int = 0):
        self.seed = seed
        self.rng = StagesSeeds(seed, verbose)
        self.verbose = verbose


class World:
    stage: List[Stage]
    seed_generator: RNG
    verbose: int

    def __init__(self, seed_generator: RNG, verbose: int = 0):
        self.seed_generator = seed_generator
        self.verbose = verbose
        self.stage = []

        verbose_str = ""
        if self.verbose > 0:
            verbose_str += "Initializing World"
        if verbose_str:
            print(verbose_str)

        self.generate_stage()

    def generate_stage(self):
        verbose_str = ""
        if self.verbose > 0:
            verbose_str += "Generating Stages"
        if verbose_str:
            print(verbose_str)

        for var in range(0, 0xD):
            self.stage.append(Stage(self.seed_generator.next(), self.verbose))
