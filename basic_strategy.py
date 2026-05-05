from environment import BlackjackEnvironment

class BasicStrategy:
    def __init__(self):
        pass

    def basic_strategy_action(self, env_copy):
        """
        Determines action using pure S17 basic strategy.
        Actions: 0 = Hit, 1 = Stand, 2 = Double Down, 3 = Split
        """
        # Gets the current state of the game from the environment
        state = env_copy.get_state() 
        player_score = state[0]
        dealer_upcard = state[1]
        usable_ace = state[2]
        can_double = state[3]
        can_split = state[4]

        # Boolean check for the ability to split
        def is_pair():
            return can_split

        # Boolean check for a "soft" hand (a hand with an ace valued as 11 where it could also be evaluated as 1)
        def is_soft():
            return usable_ace and player_score <= 21

        # Splitting Logic according to the basic strategy chart available online.
        if is_pair():
            pair_card = player_score // 2 if player_score != 22 else 11
            split_chart = {
                2:  [False, False, True, True, True, True, False, False, False, False],
                3:  [False, False, True, True, True, True, False, False, False, False],
                4:  [False, False, False, True, True, False, False, False, False, False],
                5:  [False] * 10,
                6:  [False, True, True, True, True, False, False, False, False, False],
                7:  [True, True, True, True, True, False, False, False, False, False],
                8:  [True] * 10,
                9:  [True, True, True, True, True, False, True, True, False, False],
                10: [False] * 10,
                11: [True] * 10,
            }
            if pair_card in split_chart and split_chart[pair_card][dealer_upcard - 2]:
                return 3  # Split

        # Soft Totals Action logic according to the basic strategy chart available online.
        if is_soft():
            soft_chart = {
                20: 1, 19: 1,
                18: 2 if 3 <= dealer_upcard <= 6 and can_double else (1 if dealer_upcard <= 8 else 0),
                17: 2 if 3 <= dealer_upcard <= 6 and can_double else 0,
                16: 2 if 4 <= dealer_upcard <= 6 and can_double else 0,
                15: 2 if 4 <= dealer_upcard <= 6 and can_double else 0,
                14: 2 if 5 <= dealer_upcard <= 6 and can_double else 0,
                13: 2 if 5 <= dealer_upcard <= 6 and can_double else 0,
            }
            return soft_chart.get(player_score, 0)

        # Hard Total action logic according to the basic strategy chart available online.
        if player_score >= 17: return 1  # Stand
        if 13 <= player_score <= 16 and dealer_upcard <= 6: return 1
        if player_score == 12 and 4 <= dealer_upcard <= 6: return 1
        if player_score == 11: return 2 if can_double else 0
        if player_score == 10 and dealer_upcard <= 9: return 2 if can_double else 0
        if player_score == 9 and 3 <= dealer_upcard <= 6: return 2 if can_double else 0
        return 0  # Default to Hit