import random

class BlackjackEnvironment:

    # Initializes the game environment with a balance and resets the game state to the default.
    # Balance is arbtrarily set to 20 for the sake of this example
    def __init__(self):
        self.balance = 20
        self.reset_game()

    # Generates 6 full decks of cards, shuffles them, and returns the deck
    def create_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♦', '♣']
        deck = [rank + suit for _ in range(6) for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck
    
    # Deals the cards from the deck
    def deal_card(self):
        if not self.deck:
            self.deck = self.create_deck()
        card = self.deck.pop()
        self.used_tracker.append(card)
        return card

    # Calculates the score of a hand of cards
    def calculate_score(self, hand):
        score, aces = 0, 0
        for card in hand:
            val = card[:-1]
            if val.isdigit():
                score += int(val)
            elif val in ['J', 'Q', 'K']:
                score += 10
            elif val == 'A':
                score += 11
                aces += 1
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    # Resets the game state to the initial conditions - this includes re-shuffling a new 6-deck cumulative deck of cards
    def reset_game(self):
        self.deck = self.create_deck()
        self.used_tracker = []
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.split_hands = []
        self.current_hand_index = 0
        self.split_counter = 0
        self.ace_split_used = False
        self.game_over = False
        self.result = ""
        self.bets = [1]
        if self.balance < 0:
            raise ValueError("Insufficient balance to play. Please add funds.")

    # This method is called when the player hits (draws a card)
    def hit(self):
        if self.game_over:
            return
        self.player_hand.append(self.deal_card())
        if self.calculate_score(self.player_hand) > 21:
            self.next_split_hand()

    # This method is called when the player stands (ends their turn)
    def stand(self):
        if self.game_over:
            return
        self.next_split_hand()

    # This method is called when the player doubles down (doubles their bet and draws one more card)
    def double_down(self):
        if self.game_over or len(self.player_hand) != 2:
            return
        self.balance -= 1
        self.bets[self.current_hand_index] *= 2
        self.player_hand.append(self.deal_card())
        self.next_split_hand()


    # This method is called when the player splits their hand (divides their hand into two separate hands)
    def split(self):
        if self.game_over or self.split_counter >= 3:
            return
        first_card = self.player_hand[0]
        second_card = self.player_hand[1]
        if first_card[:-1] != second_card[:-1]:
            return
        is_ace = first_card[:-1] == 'A'
        if is_ace and self.ace_split_used:
            return
        if is_ace:
            self.ace_split_used = True
            self.split_counter = 3
        self.split_hands = [[first_card, self.deal_card()], [second_card, self.deal_card()]]
        self.bets = [self.bets[0], self.bets[0]]
        self.balance -= self.bets[0]
        self.current_hand_index = 0
        self.player_hand = self.split_hands[0]


    # This method is called to move to the next split hand
    def next_split_hand(self):
        if self.split_hands and self.current_hand_index + 1 < len(self.split_hands):
            self.current_hand_index += 1
            self.player_hand = self.split_hands[self.current_hand_index]
        else:
            self.dealer_play()

    # This method is called to play out the game for the dealer after the player has finished their turn
    def dealer_play(self):
        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())
        self.game_over = True
        self.rewards = self.determine_result()


    # This method determines the result of the game based on the player's and dealer's hands (including splits)
    def determine_result(self):
        hands = self.split_hands if self.split_hands else [self.player_hand]
        total_reward = 0
        messages = []
        for i, hand in enumerate(hands):
            player_score = self.calculate_score(hand)
            dealer_score = self.calculate_score(self.dealer_hand)
            bet = self.bets[i] if i < len(self.bets) else 1
            label = f"Hand {i + 1}: " if len(hands) > 1 else ""

            if player_score > 21:
                messages.append(f"{label}Player busts! Dealer wins.")
                total_reward -= 1
            elif dealer_score > 21 or player_score > dealer_score:
                self.balance += 2 * bet
                messages.append(f"{label}Player wins!")
                total_reward += 1
            elif dealer_score > player_score:
                messages.append(f"{label}Dealer wins.")
                total_reward -= 1
            else:
                self.balance += bet
                messages.append(f"{label}Push (tie).")

        self.result = "\n".join(messages)
        return total_reward
    

    # This method is called to take the action on the state
    def step(self, action):
        if self.game_over:
            return self.get_state(), 0, True, {}
        if action == 0:
            self.hit()
        elif action == 1:
            self.stand()
        elif action == 2:
            self.double_down()
        elif action == 3:
            self.split()
        if self.game_over:
            return self.get_state(), self.rewards, True, {}
        return self.get_state(), 0, False, {}


    # This method returns the features of the current state of the game
    def get_state(self):
        player_score = self.calculate_score(self.player_hand)
        val = self.dealer_hand[0][:-1]
        dealer_upcard = 11 if val == 'A' else 10 if val in ['J', 'Q', 'K'] else int(val)
        if (self.player_hand[0] == 'A' and self.player_hand[1] == 'A'):
            usable_ace = 2
        elif any(card[:-1] == 'A' for card in self.player_hand):
            usable_ace = 1
        else:
            usable_ace = 0

        num_player_hands = len(self.split_hands) if self.split_hands else 1
        if num_player_hands > 1:
            active_hand = self.split_hands[self.current_hand_index]
            player_score = self.calculate_score(active_hand)

        can_double = len(self.player_hand) == 2 and self.balance >= self.bets[self.current_hand_index] * 2
        first_card = self.player_hand[0]
        second_card = self.player_hand[1]
        can_split = first_card[:-1] == second_card[:-1] and not self.ace_split_used
        current_hand_index = self.current_hand_index if self.split_hands else 0

        return [player_score, dealer_upcard, usable_ace, can_double, can_split,
                num_player_hands, self.balance, self.bets[self.current_hand_index], current_hand_index]