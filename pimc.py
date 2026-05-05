from environment import BlackjackEnvironment as env
from math import inf, sqrt, log
import random
import copy

'''
This is a PIMC agent for Blackjack. It uses a predetermined deck of cards to simulate the game and make decisions based on the basic strategy. The agent plays multiple trials to determine the best action to take in a given state.
'''
class Node:
    def __init__(self, env, numberofTrials=1000):
        self.env = env
        self.numberofTrials = numberofTrials

        # This method is called to identify the cards that are still potentially available for us.
    def guess_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♦', '♣']
        full_deck = [rank + suit for _ in range(6) for rank in ranks for suit in suits]
        available_cards = [card for card in full_deck if card not in self.env.used_tracker]
        random.shuffle(available_cards)
        return available_cards
    
    # We choose the next 30 cards from the deck in order to make it clear that we know what we are choosing from.
    def predetermined_deck(self):
        return self.guess_deck()[0:30]

    # This method uses the "guessed" deck to create a perfect information environment.
    def determined_state(self, env_copy):
        dealer_up = env_copy.dealer_hand[0]
        guessed_card = self.predetermined_deck()[0]
        env_copy.dealer_hand = [dealer_up, guessed_card]
        return env_copy
    

    # This method uses the determined state and makes informed decisions based on predicted values and outcomes.
    def basic_strategy_action(self, env_copy):
        state = env_copy.get_state()
        player_score = state[0]
        dealer_upcard = state[1]
        usable_ace = state[2]
        can_double = state[3]
        can_split = state[4]

        next_card = self.predetermined_deck()[0]
        next_val = next_card[:-1]
        next_value = 11 if next_val == 'A' else 10 if next_val in ['J', 'Q', 'K'] else int(next_val)

        def is_pair():
            return can_split

        def is_soft():
            return usable_ace and player_score <= 21

        # OVERRIDES basic strategy using the next card value to calculate potential player score
        if player_score + next_value == 21:
            if can_double and len(env_copy.player_hand) == 2:
                return 2
            return 0

        if player_score >= 17 and player_score + next_value <= 21:
            return 0

        if can_double and len(env_copy.player_hand) == 2:
            if player_score in [9, 10, 11] and next_value == 10:
                return 2

        # Default Basic Strategy splitting logic
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
                return 3

        # Action to take if the hand has an ace.
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

        if player_score >= 17: return 1
        if 13 <= player_score <= 16 and dealer_upcard <= 6: return 1
        if player_score == 12 and 4 <= dealer_upcard <= 6: return 1
        if player_score == 11: return 2 if can_double else 0
        if player_score == 10 and dealer_upcard <= 9: return 2 if can_double else 0
        if player_score == 9 and 3 <= dealer_upcard <= 6: return 2 if can_double else 0
        return 0
    

    # This method executes the PIMC algorithm to determine the best action to take in a given state.
    def pimc_agent(self):
        action_rewards = {0: 0, 1: 0, 2: 0, 3: 0}
        action_count = {0: 0, 1: 0, 2: 0, 3: 0}

        for trial in range(self.numberofTrials):
            env_copy = copy.deepcopy(self.env)
            env_copy = self.determined_state(env_copy)

            for action in [0, 1, 2, 3]:
                test_env = copy.deepcopy(env_copy)
                reward = 0

                try:
                    _, _, done, _ = test_env.step(action)
                    while not done:
                        bs_action = self.basic_strategy_action(test_env)
                        _, reward, done, _ = test_env.step(bs_action)
                except Exception as e:
                    continue

                action_rewards[action] += reward
                action_count[action] += 1

        best_action = max(action_rewards, key=lambda a: action_rewards[a] / (action_count[a] or 1))
        return best_action
