import tkinter as tk
from environment import BlackjackEnvironment
from pimc import Node
from basic_strategy import BasicStrategy


class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.env = BlackjackEnvironment()

        self.canvas = tk.Canvas(root, width=800, height=800, bg="green")
        self.canvas.pack()

        self.hit_button = tk.Button(root, text="Hit", command=self.hit, font=("Gotham", 12, "bold"))
        self.stand_button = tk.Button(root, text="Stand", command=self.stand, font=("Gotham", 12, "bold"), background="red")
        self.split_button = tk.Button(root, text="Split", command=self.split, font=("Gotham", 12))
        self.double_down_button = tk.Button(root, text="Double Down", command=self.double_down, font=("Gotham", 12))
        self.new_game_button = tk.Button(root, text="New Game", command=self.new_game, font=("Gotham", 12, "bold"), background="gray")
        self.root.bind("<Right>", self.call_pimc_agent)
        self.root.bind("<Left>", self.call_basic_strategy_agent)


        self.new_game()

    def display_card(self, card, x, y):
        self.canvas.create_rectangle(x, y, x + 50, y + 80, fill="white")
        self.canvas.create_text(x + 25, y + 20, text=card[:-1], font=("Arial", 12))
        color = "red" if card[-1] in ['♥', '♦'] else "black"
        self.canvas.create_text(x + 25, y + 50, text=card[-1], font=("Arial", 16), fill=color)

    def display_hand(self, hand, x, y, hidden=False):
        for i, card in enumerate(hand):
            if hidden and i == 0:
                self.canvas.create_rectangle(x + i * 60, y, x + i * 60 + 50, y + 80, fill="gray")
                self.canvas.create_text(x + i * 60 + 25, y + 40, text="?", font=("Arial", 20))
            else:
                self.display_card(card, x + i * 60, y)

    def redraw(self, show_dealer=False):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 800, 800, fill="green")
        self.canvas.create_text(700, 30, text=f"Balance: ${self.env.balance}", font=("Arial", 14, "bold"), fill="white")

        # Dealer's hand
        self.canvas.create_text(100, 20, text="Dealer", font=("Arial", 14, "bold"))
        dealer_hidden = not show_dealer and not self.env.game_over
        self.display_hand(self.env.dealer_hand, 340, 60, hidden=dealer_hidden)

        # Player hands
        if self.env.split_hands:
            for i, hand in enumerate(self.env.split_hands):
                y_position = 380 + i * 100
                script = self.env.get_state()
                label = f"Hand {i + 1}" + (" (Active); Current Value: " + str(script[0]) if i == self.env.current_hand_index else "")
                self.canvas.create_text(100, y_position, text=label, font=("Arial", 12))
                self.display_hand(hand, 340, y_position)
        else:
            script = self.env.get_state()
            self.canvas.create_text(100, 380, text= f"Your Hand; Current Value: " + str(script[0]), font=("Arial", 12))
            self.display_hand(self.env.player_hand, 340, 380)

        # Buttons
        self.canvas.create_window(280, 600, window=self.hit_button)
        self.canvas.create_window(360, 600, window=self.stand_button)
        self.canvas.create_window(440, 600, window=self.new_game_button)
        self.canvas.create_window(520, 600, window=self.split_button)
        self.canvas.create_window(600, 600, window=self.double_down_button)

        # Game result or status
        if self.env.game_over:
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.split_button.config(state=tk.DISABLED)
            self.double_down_button.config(state=tk.DISABLED)
            self.canvas.create_text(400, 300, text=self.env.result, font=("Arial", 16, "bold"))
        else:
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.split_button.config(state=tk.NORMAL)
            self.double_down_button.config(state=tk.NORMAL)
            self.canvas.create_text(400, 300, text="Your Turn", font=("Arial", 16))

    def new_game(self):
            self.env.balance -= 1  # Deduct the $1 bet
            self.env.reset_game()
            self.redraw()

        # Run PIMC agent to take the first action
        #agent = Node(self.env, numberofTrials=200)
        #first_action = agent.pimc_agent()
        #self.env.step(first_action)

        # Let basic strategy complete the round
    '''
        while not self.env.game_over:
            action = agent.basic_strategy_action(self.env)
            self.env.step(action)

    self.redraw(show_dealer=True)
    '''

        
    def hit(self):
        self.env.hit()
        self.redraw()

    def stand(self):
        self.env.stand()
        self.redraw(show_dealer=True)

    def split(self):
        self.env.split()
        self.redraw()

    def double_down(self):
        self.env.double_down()
        self.redraw(show_dealer=True)

    def call_pimc_agent(self, event):
        agent = Node(self.env)
        action = agent.pimc_agent()
        self.env.step(action)
        self.redraw(show_dealer=self.env.game_over)

    def call_basic_strategy_agent(self, event):
        agent = BasicStrategy()
        action = agent.basic_strategy_action(self.env)
        self.env.step(action)
        self.redraw(show_dealer=self.env.game_over)


if __name__ == "__main__":
    root = tk.Tk()
    BlackjackGUI(root)
    root.mainloop()