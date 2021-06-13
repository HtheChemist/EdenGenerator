from game import Game
from rng import GameSeeds, DropSeeds, ItemsSeeds, PillsSeeds, CardsSeeds, PickupSeeds1, PickupSeeds2, CardsDrop, \
    PillsDrop
from seeds import seed2string
from pools import ItemType, isaac_items, items_blacklist

verbose_level = 0

def bruteforce(start: int = 0):
    # I am at 1561700
    for seed in range(start, 0xFFFFFFFF + 1):
        if not seed % 100:
            print(
                str(seed)
                + "/"
                + str(0xFFFFFFFF)
                + " ("
                + str(round(seed / 0xFFFFFFFF * 100, 3))
                + "%)"
            )
        game = Game(seed, verbose_level)
        # if game.eden.card == 73:
        if (
                game.eden.active == 352
                and game.eden.passive == 432
                and game.eden.card == 73
        ):
            game.print_seed()
            game.eden.print_stats()
            break

class Reverser:
    collectibles_number = 0x2DA
    
    def __init__(self, active: int = None, passive: int = None, card: int = None, trinket: int = None, pill_effect: int = None, start_seed: int = 0):
        self.potential_dropseed = None
        self.potential_holdseed = None
        self.potential_trinketseed = None
        self.potential_nothingseed = None
        self.start_seed = start_seed
        self.active = active
        self.passive = passive
        self.card = card
        self.pill_effect = pill_effect
        self.trinket = trinket
        self.trinket_found = False
        self.passive_found = False
        self.active_found = False
        self.hold_found = False
        self.hold_type = None
        self.hold_seed = None
        self.trinket_seed = None
        self.nothing_seed = None
    
    @property
    def min_item(self):
        if self.active and self.passive:
            return self.active if self.active < self.passive else self.passive
        elif self.active:
            return self.active
        elif self.passive:
            return self.passive
        else:
            return None

    @property
    def max_item(self):
        if self.active and self.passive:
            return self.active if self.active > self.passive else self.passive
        return None
    
    @property
    def min_found(self):
        if self.active and self.passive:
            return self.active_found if self.active < self.passive else self.passive_found
        elif self.active:
            return self.active_found
        elif self.passive:
            return self.passive_found
        else:
            return None

    @property
    def max_found(self):
        if self.active and self.passive:
            return self.active_found if self.active > self.passive else self.passive_found
        return None

    @staticmethod
    def check_item_type(item_id):
        item_type = None
        try:
            item_type = isaac_items[item_id]
        except KeyError:
            return ItemType.Forbidden
        
        if item_type == ItemType.Active:
            return ItemType.Active
        else:
            return ItemType.Passive
   
    def reverse(self):
        while self.start_seed < 0xFFFFFFFF:
            print('Trying seed: ' + str(hex(self.start_seed)))
            item_id = self.start_seed % self.collectibles_number + 1
            if item_id == self.min_item or item_id == self.max_item:
                if self.check_item_type(item_id) == ItemType.Active:
                    first_item_type = self.check_item_type(item_id)
                    self.active_found = True
                else:
                    first_item_type = self.check_item_type(item_id)
                    self.passive_found = True

                print('First item found: ' + str(item_id) + ' (' + str(first_item_type) + ')')
                self.potential_dropseed = DropSeeds(self.start_seed)
                for i in range(0, 99):
                    item_id = self.potential_dropseed.revese_random(self.collectibles_number) + 1
                    if item_id not in items_blacklist:
                        if self.check_item_type(item_id) == first_item_type:
                            print('Another ' + str(first_item_type) + ' was found before the second one. Break.')
                            break
                        else:
                            if item_id == self.min_item or item_id == self.max_item:
                                print('Second item found: ' + str(item_id))
                                if self.check_item_type(item_id) == ItemType.Active:
                                    self.active_found = True
                                else:
                                    self.passive_found = True
                                break

                if self.passive_found and self.active_found:
                    
                    check_point_1 = self.potential_dropseed.previous()
                    check_point_2 = self.potential_dropseed.previous()
                    check_point_3 = self.potential_dropseed.previous()
                    check_point_4 = self.potential_dropseed.previous()
                    check_point_5 = self.potential_dropseed.previous()

                    # Check if with trinket
                    if not check_point_1 % 3 and self.trinket is not None:
                        print('Trinket possible')
                        self.potential_trinketseed = DropSeeds(check_point_1)
                        if self.get_trinket():
                            self.trinket_seed = self.goto_start_seed('trinket', check_point_2)
                            self.print_stats(self.trinket_seed)
                            break
                        else:
                            print('This try will not yield the right trinket. Next.')
                    elif self.trinket is not None:
                        print('This try will not yield any trinket. Next')
                        
                    # Check if with card or pill
                    if self.card is not None or self.pill_effect is not None:
                        if check_point_2 & 1 and not check_point_3 & 1 and check_point_4 % 3:
                            print('Pill possible')
                            if self.pill_effect is not None:
                                self.potential_holdseed = PillsDrop(check_point_1)
                                self.hold_type = 'pill'
                                if self.get_pill():
                                    self.hold_seed = self.goto_start_seed('card', check_point_5)
                                    self.print_stats(self.hold_seed)
                                    break
                                else:
                                    print('This try will not yield the right pill. Next.')
                            else:
                                print('This try will not yield a card. Next.')
                        elif not check_point_2 & 1 and not check_point_3 & 1 and check_point_4 % 3:
                            print('Card possible')
                            if self.card is not None:
                                self.potential_holdseed = CardsDrop(check_point_1,2)
                                self.hold_type = 'card'
                                if self.get_card():
                                    self.hold_seed = self.goto_start_seed('card', check_point_5)
                                    self.print_stats(self.hold_seed)
                                    break
                                else:
                                    print('This try will not yield the right card. Next')
                            else:
                                print('This try will not yield a pill. Next.')
                                
                    # Check if it will yield nothing
                    if check_point_1 & 1 and check_point_2 % 3:
                        print('Theoretically nothing')
                        if self.card is None and self.pill_effect is None and self.trinket is None:
                            self.nothing_seed = self.goto_start_seed('nothing', check_point_3)
                            self.print_stats(self.nothing_seed)
                            break
                        else:
                            print('This try will yield a pill, card or trinket. Next')
                            
            print('The items are not found according to the asked requirement. Resetting.')
            # break
            self.passive_found = False
            self.active_found = False
            self.potential_dropseed = None
            self.start_seed += self.calculate_next_step()
            
    def calculate_next_step(self):
        modulo = self.start_seed % self.collectibles_number
        if modulo + 1 < self.min_item:
            return self.min_item - modulo - 1
        elif self.min_item <= modulo + 1 < self.max_item:
            return self.max_item - modulo - 1
        else:
            return self.collectibles_number - modulo + self.min_item - 1
        
    def goto_start_seed(self, type, seed):
        items_seeds = ItemsSeeds(seed, 2)
        items_seeds.previous()
        items_seeds.previous()
        items_seeds.previous()
        items_seeds.previous()
        game_seeds = GameSeeds(items_seeds.previous())
        game_seeds.previous()
        for var in range(0, 0xD):
            game_seeds.previous()
        return game_seeds.previous()
    
    def get_trinket(self):
        self.potential_trinketseed = ItemsSeeds(self.potential_trinketseed.previous())
        self.potential_trinketseed.previous()
        self.potential_trinketseed.previous()
        self.potential_trinketseed.previous()
        self.potential_trinketseed.previous()
        self.potential_trinketseed = GameSeeds(self.potential_trinketseed.previous())
        self.potential_trinketseed.next()
        self.potential_trinketseed = PickupSeeds1(self.potential_trinketseed.next())
        self.potential_trinketseed = PickupSeeds2(self.potential_trinketseed.next())
        trinket_id = self.potential_trinketseed.random(0xBE)
        if trinket_id == self.trinket or self.trinket == -1:
            self.trinket_found = True
            self.trinket = trinket_id
            return True
        else:
            return False
    
    def get_card(self):
        if self.potential_holdseed.random(0x19):
            tmp_card = self.potential_holdseed.random(0x16) + 1
            if not self.potential_holdseed.random(7):
                tmp_card += 55
        else:
            tmp_card = -1
            pass
        if self.card == tmp_card or self.card == -1:
            return True
        else:
            return False
    
    def get_pill(self):
        return True
    
    # def generate_different_option(self):
    #     # To trinket
    #     if self.trinket is not None and self.card is None and self.pill_effect is None:
    #         with_trinket_seed = DropSeeds(self.potential_dropseed.seed)
    #         start_seed = self.from_eden_seed_to_start_seed(with_trinket_seed.previous())
    #         print('With trinket: ' + str(start_seed) + ' (' + seed2string(start_seed) + ')')
    #
    #     with_hold_seed = DropSeeds(self.potential_dropseed.seed)
    #     hold_seed_value = with_hold_seed.previous().seed
    #     if with_hold_seed.previous() & 1:
    #         self.potential_holdseed = PillsSeeds(hold_seed_value)
    #     else:
    #         self.potential_holdseed = CardsSeeds(hold_seed_value)
    #     hold_seed_value.previous()
    #     start_seed = self.from_eden_seed_to_start_seed(hold_seed_value.previous())
    #     print('With card: ' + str(start_seed) + ' (' + seed2string(start_seed) + ')')
    #
    #     # Bug here
    #     if self.trinket is None and self.card is None and self.pill_effect is None:
    #         with_nothing_seed = DropSeeds(self.potential_dropseed.seed,2)
    #         with_nothing_seed.previous()
    #         start_seed = self.from_eden_seed_to_start_seed(with_nothing_seed.previous())
    #         print('With nothing: ' + str(start_seed) + ' (' + seed2string(start_seed) + ')')
    
    def print_stats(self, seed):
        print("--- Seed ---")
        print(seed2string(seed) + " (" + str(seed) + ")")
        print("--- Eden ---")
        # print("Red Hearts: " + str(self.red_hearts))
        # print("Soul Hearts: " + str(self.soul_hearts))
        # print("")
        print("Trinket: " + str(self.trinket))
        print("Card/Soul/Pill: " + str(self.card))
        print("Active: " + str(self.active))
        print("Passive: " + str(self.passive))
        # print("")
        # print("Damage delta: " + str(self.damage_delta))
        # print("Speed delta: " + str(self.speed_delta))
        # print("Tear delta: " + str(self.tear_delta))
        # print("Range delta: " + str(self.range_delta))
        # print("Speed delta: " + str(self.speed_delta))
        # print("Luck delta: " + str(self.luck_delta))
        
        
            
    


if __name__ == "__main__":
    # reverser = Reverser(active=325, passive=389, start_seed=0xf7a82728)
    reverser = Reverser(active=325, passive=389, card=12, start_seed=0x0)
    reverser.reverse()

    # game = Game(93001831, 2)
    # game.print_seed()
    # game.eden.print_stats()

# # print('Stage Generation')
# # for stage in stages_seeds:
# #     stage.next() # This one set the stage type
# #     stage.next()
# #     # Missing a lot of these will come back later
# #     # stage.print_seed()
#
#
# verbose = 0
# print('Pill RNG Loop?')
# for var in range(0, 31):
#     pickup_seeds.next()
#     pickup_seeds.next()
# pickup_seeds.genrand(0x270)
# for var in range(0, 12):
#     pickup_seeds.next()
#
#
# print('New some RNG from start seed')
# unknown_seeds_2 = RNG(0x459, [0x3, 0xD, 0x7])
# unknown_seeds_2.next()
# unknown_seeds_2_array = []
# for var in range(0, 0x25): #Pool Seeds?
#     # Pool 0 = Treasure
#     unknown_seeds_2_array.append(RNG(unknown_seeds_2.next(), [0x3, 0xD, 0x7]))
#     unknown_seeds_2_array[var].genrand(0x270)
