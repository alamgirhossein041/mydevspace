import numpy as np
import random
import sys
import pandas as pd


class Agathion:
    chances = [1, 1, 1, 0.65, 0.55, 0.5, 0.3, 0.25, 0.2, 0.15]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class VenirTalisman:
    chances = [0.66, 0.66, 0.66, 0.66, 0.66, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.35, 0.35, 0.35, 0.35, 0.5,
               0.35, 0.35, 0.35, 0.35, 0.35, 0.5, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class Brooch:
    chances = [0.25, 0.25, 0.25, 0.25]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class Stones:
    chances = [0.65, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class CircletHero:
    chances = [0.66, 0.6, 0.55, 0.45, 0.4, 0.35, 0.26, 0.24, 0.22, 0.2]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class Dolls:
    chances = [0.4, 0.7]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class Cloak:
    chances = [0.85, 0.8, 0.75, 0.6, 0.55, 0.5, 0.4, 0.25, 0.2, 0.15]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class EinhasadPendant:
    chances = [0.5, 0.5, 0.5, 0.4]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class DragonBelt:
    chances = [0.60, 0.5, 0.40, 0.35, 0.3, 0.28, 0.26, 0.24, 0.22, 0.2]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class EpicJewelery:
    chances = [1, 0.5, 0.4, 0.3, 0.2]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class AdenTalisman:
    chances = [1, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.24, 0.16, 0.1, 0.1]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class EvaTalisman:
    chances = [0.6, 0.5, 0.4, 0.35, 0.3, 0.28, 0.26, 0.24, 0.22, 0.2]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class AuthorityTalisman:
    chances = [0.6, 0.5, 0.4, 0.35, 0.3, 0.28, 0.26, 0.24, 0.22, 0.2]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class SpeedTalisman:
    chances = [0.6, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.12]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class BaiumTalisman:
    chances = [0.9, 0.8, 0.7, 0.3, 0.15]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class AdenCrystal:
    chances = [0.7, 0.6, 0.5, 0.4, 0.6, 0.55, 0.5, 0.45, 0.4, 0.5, 0.45, 0.4, 0.3, 0.3, 0.25, 0.2, 0.2, 0.15, 0.1]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class HardinCrystal:
    chances = [0.6, 0.55, 0.5, 0.45, 0.45, 0.4, 0.35, 0.3, 0.25, 0.35, 0.3, 0.25, 0.2, 0.15, 0.25, 0.2, 0.15, 0.1, 0.05]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


class EvolutionRune:
    chances = [0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35]

    def __init__(self):

        self.level = 0

    def enchant(self):

        for chance in self.chances:

            if chance > random.uniform(0, 1):

                self.level += 1

            else:

                return self.level

        return self.level


def enchant_items(item_type, nr_enchants):
    rolls = int(nr_enchants)

    enchants = []

    for i in range(rolls):
        # create one enchant roll and append to list enchants
        enchanting_result = eval(item_type)().enchant()
        enchants.append(enchanting_result)

    labels = np.unique(enchants)

    occurencies = []
    for label in labels:
        occurencies.append(enchants.count(label))

    return occurencies, labels.tolist()


def enchant_experiment(item_type, available_items):
    nr_of_experiments = 5000

    max_enchants = []
    for _ in range(nr_of_experiments):
        occurencies, labels = enchant_items(item_type, available_items)

        max_enchants.append(max(labels, default=0))

    max_achieved_enchant = max(max_enchants, default=0)

    enchant_levels = []
    success_rates = []

    for n in range(max_achieved_enchant):
        nr_of_success_ench = len([i for i in max_enchants if i >= n])

        enchant_levels.append(n)
        success_rates.append(nr_of_success_ench / nr_of_experiments)

    d = {'Enchant level': enchant_levels, 'Success rate': success_rates}
    df = pd.DataFrame(d)
    df['Enchant level'] = df['Enchant level'].astype(str)
    df['Success rate'] = df['Success rate'].map(lambda n: '{:,.2%}'.format(n)).astype(str)
    return df


if __name__ == '__main__':

    item_type = 'DragonBelt'
    available_items = 5
    nr_of_experiments = 1000

    max_enchants = []
    for _ in range(nr_of_experiments):
        occurencies, labels = enchant_items(item_type, available_items)

        max_enchants.append(max(labels, default=0))

    max_achieved_enchant = max(max_enchants, default=0)

    enchant_levels = []
    success_rates = []

    for n in range(max_achieved_enchant):
        nr_of_success_ench = len([i for i in max_enchants if i >= n])

        enchant_levels.append(n)
        success_rates.append(nr_of_success_ench / nr_of_experiments)

    d = {'Enchant level': enchant_levels, 'Success rate': success_rates}
    df = pd.DataFrame(d)
    df['Enchant level'] = df['Enchant level'].astype(str)
    df['Success rate'] = df['Success rate'].map(lambda n: '{:,.2%}'.format(n)).astype(str)
    print(df)
