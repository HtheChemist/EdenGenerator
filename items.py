from typing import List, Type

from rng import RNG

# Unsure what this does, it is in the decompiled code in some way. I would guess that it is used to generate which item
# is spawned in each rooms/drop

class Item:
    uid: int
    seed: int
    verbose: int
    name: str

    def __init__(self, uid: int, seed: int, verbose: int = 0):
        self.uid = uid
        self.seed = seed
        self.verbose = verbose

        verbose_str: str = ""
        if verbose > 2:
            verbose_str += (
                "Item id: " + str(self.uid) + " (Seed: " + str(hex(self.seed)) + ")"
            )


class Collectible(Item):
    name: str = "Collectible"


class Pill(Item):
    name: str = "Pill"


class Trinket(Item):
    name: str = "Trinket"


class Card(Item):
    name: str = "Card"


class ItemsArray:
    item_class: Type[Item]
    size: int

    def __init__(self, seed_generator: RNG, verbose: int = 0):
        if not hasattr(self, "item_class"):
            raise AttributeError("Base class cannot be instanced directly")

        self.seed_generator = seed_generator
        self.verbose = verbose
        self.items: List[Item] = []

        verbose_str: str = ""
        if verbose > 0:
            verbose_str += "Generating Items Array: " + self.__class__.__name__

        if verbose_str:
            print(verbose_str)

        for var in range(0, self.size):
            self.items.append(
                self.item_class(var, self.seed_generator.next(), self.verbose)
            )


class CollectiblesArray(ItemsArray):
    item_class: Type[Item] = Collectible
    size: int = 0x2DB


class TrinketsArray(ItemsArray):
    item_class: Type[Item] = Trinket
    size: int = 0xBE


class PillsArray(ItemsArray):
    item_class: Type[Item] = Pill
    size: int = 0x32


class CardsArray(ItemsArray):
    item_class: Type[Item] = Card
    size: int = 0x62
