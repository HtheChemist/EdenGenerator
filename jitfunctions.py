import numpy as np
import numba
from jitpools import isaac_items


@numba.njit
def next_xorshift(
    seed: numba.uint32, shift1: numba.uint32, shift2: numba.uint32, shift3: numba.uint32
):
    seed ^= numba.uint32(seed >> shift1)
    # print(seed)
    seed ^= numba.uint32(seed << shift2)
    # print(seed)
    seed ^= numba.uint32(seed >> shift3)
    return numba.uint32(seed)


@numba.njit
def previous_xorshift(
    seed: numba.uint32, shift1: numba.uint32, shift2: numba.uint32, shift3: numba.uint32
):
    seed = reverse_xor_rshift(seed, shift3)
    # print(seed)
    seed = reverse_xor_lshift(seed, shift2)
    # print(seed)
    seed = reverse_xor_rshift(seed, shift1)
    return numba.uint32(seed)


@numba.njit
def reverse_xor_lshift(seed: numba.uint32, shift: numba.uint32):
    i: numba.uint32 = shift
    while i < 32:
        seed ^= numba.uint32(seed << i)
        i *= 2
    return numba.uint32(seed)


@numba.njit
def reverse_xor_rshift(seed: numba.uint32, shift: numba.uint32):
    seed = reverse_seed(seed)
    seed = reverse_xor_lshift(seed, shift)
    seed = reverse_seed(seed)
    return numba.uint32(seed)


@numba.njit
def reverse_seed(seed: numba.uint32):
    bin_str: np.ndarray = np.zeros(32, dtype=numba.uint32)
    matrix: np.ndarray = 1 << np.arange(bin_str.size, dtype=numba.uint32)
    matrix = np.flip(matrix)
    i: int = 0
    num: numba.uint32 = 0
    while i < 32:
        num = num + (seed % 2) * matrix[i]
        seed = seed // 2
        i += 1
        if seed < 1:
            break
    return numba.uint32(num)


@numba.njit
def reverser(
    active: int = 0,
    passive: int = 0,
    card: int = 0,
    trinket: int = 0,
    pill_effect: int = 0,
    start_seed: int = 0,
    end_seed: int = 0xFFFFFFFF,
):

    collectibles_number = 0x2DA
    trinket_number = 0xBE
    card_number = 0x16

    potential_drop_seed: numba.uint32 = 0
    potential_hold_seed: numba.uint32 = 0
    potential_trinket_seed: numba.uint32 = 0
    potential_nothing_seed: numba.uint32 = 0

    start_seed: numba.uint32 = start_seed
    current_seed: numba.uint32 = start_seed
    end_seed: numba.uint32 = end_seed
    active = active
    passive = passive
    card = card
    pill_effect = pill_effect
    trinket = trinket
    trinket_found: numba.boolean = False
    passive_found: numba.boolean = False
    active_found: numba.boolean = False
    hold_found: numba.boolean = False

    hold_type: numba.uint32 = None

    hold_seed: numba.uint32 = None
    trinket_seed: numba.uint32 = None
    nothing_seed: numba.uint32 = None

    drop_seed: numba.uint32 = 0
    first_item_type: numba.uint32 = -1

    if active < passive:
        min_item = active
        max_item = passive
    else:
        min_item = passive
        max_item = active

    found_seed = []

    while current_seed < end_seed:
        # print('Trying seed: ' + str(hex(self.start_seed)))
        item_id = current_seed % collectibles_number + 1
        if item_id == min_item or item_id == max_item:
            if isaac_items[item_id] == 1:
                first_item_type = 1
                active_found = True
            else:
                first_item_type = 0
                passive_found = True

            # print('First item found: ' + str(item_id) + ' (' + str(first_item_type) + ')')
            drop_seed = current_seed
            for i in range(0, 99):
                drop_seed = previous_xorshift(drop_seed, 0x1, 0x5, 0x13)
                item_id = drop_seed % collectibles_number + 1
                if isaac_items[item_id] > -1:
                    if isaac_items[item_id] == first_item_type:
                        # print('Another ' + str(first_item_type) + ' was found before the second one. Break.')
                        break
                    else:
                        if item_id == min_item or item_id == max_item:
                            # print('Second item found: ' + str(item_id))
                            if isaac_items[item_id] == 1:
                                active_found = True
                            else:
                                passive_found = True
                            break

            if passive_found and active_found:

                check_point_1 = previous_xorshift(drop_seed, 0x1, 0x5, 0x13)
                check_point_2 = previous_xorshift(check_point_1, 0x1, 0x5, 0x13)
                check_point_3 = previous_xorshift(check_point_2, 0x1, 0x5, 0x13)
                check_point_4 = previous_xorshift(check_point_3, 0x1, 0x5, 0x13)
                check_point_5 = previous_xorshift(check_point_4, 0x1, 0x5, 0x13)

                # Check if with trinket
                if not check_point_1 % 3 and trinket != 0:
                    # print('Trinket possible')
                    potential_trinket_seed = check_point_1
                    if get_trinket(potential_trinket_seed, trinket, trinket_number):
                        trinket_seed = goto_start_seed(check_point_2)
                        # self.print_stats(self.trinket_seed)
                        found_seed.append(trinket_seed)
                        # break
                    else:
                        # print('This try will not yield the right trinket. Next.')
                        pass
                elif trinket != 0:
                    # print('This try will not yield any trinket. Next')
                    pass

                # Check if with card or pill
                if card != 0 or pill_effect != 0:
                    if (
                        check_point_2 & 1
                        and not check_point_3 & 1
                        and check_point_4 % 3
                    ):
                        # print('Pill possible')
                        if pill_effect != 0:
                            if get_pill(check_point_1, pill_effect):
                                hold_seed = goto_start_seed(check_point_5)
                                # self.print_stats(self.hold_seed)
                                found_seed.append(hold_seed)
                                # break
                            else:
                                # print('This try will not yield the right pill. Next.')
                                pass
                        else:
                            # print('This try will not yield a card. Next.')
                            pass
                    elif (
                        not check_point_2 & 1
                        and not check_point_3 & 1
                        and check_point_4 % 3
                    ):
                        # print('Card possible')
                        if card != 0:
                            if get_card(check_point_1, card, card_number):
                                hold_seed = goto_start_seed(check_point_5)
                                # self.print_stats(self.hold_seed)
                                found_seed.append(hold_seed)
                                # break
                            else:
                                # print('This try will not yield the right card. Next')
                                pass
                        else:
                            # print('This try will not yield a pill. Next.')
                            pass

                # Check if it will yield nothing
                if check_point_1 & 1 and check_point_2 % 3:
                    # print('Theoretically nothing')
                    if (
                        card == 0
                        and pill_effect == 0
                        and trinket == 0
                    ):
                        nothing_seed = goto_start_seed(check_point_3)
                        # self.print_stats(self.nothing_seed)
                        found_seed.append(nothing_seed)
                        # break
                    else:
                        # print('This try will yield a pill, card or trinket. Next')
                        pass

        # print('The items are not found according to the asked requirement. Resetting.')
        # break
        passive_found = False
        active_found = False
        potential_drop_seed = 0
        current_seed += calculate_next_step(current_seed, collectibles_number, min_item, max_item)

    return found_seed


@numba.njit
def calculate_next_step(current_seed, collectibles_number, min_item, max_item):
    modulo = current_seed % collectibles_number
    if modulo + 1 < min_item:
        return min_item - modulo - 1
    elif min_item <= modulo + 1 < max_item:
        return max_item - modulo - 1
    else:
        return collectibles_number - modulo + min_item - 1


@numba.njit
def goto_start_seed(seed):
    seed = previous_xorshift(seed, 0x1, 0xB, 0x10)
    seed = previous_xorshift(seed, 0x1, 0xB, 0x10)
    seed = previous_xorshift(seed, 0x1, 0xB, 0x10)
    seed = previous_xorshift(seed, 0x1, 0xB, 0x10)
    seed = previous_xorshift(seed, 0x1, 0xB, 0x10)
    for var in range(0, 0xF):
        seed = previous_xorshift(seed, 0x3, 0x17, 0x19)
    return seed

@numba.njit
def get_trinket(seed, trinket_id, trinket_number):
    seed = previous_xorshift(seed, 0x1, 0x5, 0x13)
    seed = previous_xorshift(seed, 0x1, 0xB, 0x10)
    seed = previous_xorshift(seed, 0x1, 0xB, 0x10)
    seed = previous_xorshift(seed, 0x1, 0xB, 0x10)
    seed = previous_xorshift(seed, 0x1, 0xB, 0x10)
    seed = previous_xorshift(seed, 0x1, 0xB, 0x10)
    seed = next_xorshift(seed, 0x3, 0x17, 0x19)
    seed = next_xorshift(seed, 0x3, 0x17, 0x19)
    seed = next_xorshift(seed, 0x1, 0x9, 0x1D)
    seed = next_xorshift(seed, 0x1, 0x5, 0x13)
    if seed % trinket_number == trinket_id or trinket_id == -1:
        return True
    else:
        return False

@numba.njit
def get_card(seed, card_id, card_number):
    seed = previous_xorshift(seed, 0x1, 0x5, 0x13)
    seed = next_xorshift(seed, 0x3, 0x3, 0x1D)
    if seed % 0x19:
        seed = next_xorshift(seed, 0x3, 0x3, 0x1D)
        tmp_card = seed % 0x16 + 1
        seed = next_xorshift(seed, 0x3, 0x3, 0x1D)
        if not seed % 0x7:
            tmp_card += 55
    else:
        tmp_card = -1
    print(tmp_card)
    if card_id == tmp_card or card_id == -1:
        return True
    else:
        return False

@numba.njit
def get_pill(seed, pill_effect_id):
    return True

if __name__ == "__main__":
    aa = reverser(active=352, passive=432, card=73, start_seed=0x9555ea3, end_seed=0x9990000)
    print(aa)
