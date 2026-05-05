from environment import BlackjackEnvironment
from pimc import Node
from basic_strategy import BasicStrategy  # Adjust if needed

def run_pimc_game():
    """
    Simulates one full game using the PIMC agent.
    """
    env = BlackjackEnvironment()
    node = Node(env)

    # PIMC agent chooses an action first
    action = node.pimc_agent()
    env.step(action)

    # Basic Strategy agent finishes the game for the player after initial PIMC move
    while not env.game_over:
        bs_action = node.basic_strategy_action(env)
        env.step(bs_action)

    return env.result # Results (including possible splits)

def run_basic_strategy_game():
    """
    Simulates one full game using only the Basic Strategy agent.
    """
    env = BlackjackEnvironment()
    agent = BasicStrategy()

    while not env.game_over:
        action = agent.basic_strategy_action(env)
        env.step(action)

    return env.result

def parse_results(result_text, results_dict):
    """
    Parses the result text from a game and updates the agent's statistics.
    """
    outcomes = result_text.strip().split("\n")
    hands_in_deal = len(outcomes) # How many hands were played in this deal

    # Count splits (every extra hand beyond the first indicates a split)
    if hands_in_deal > 1:
        results_dict["total_splits"] += hands_in_deal - 1

    # Evaluate the outcome of each hand individually
    for outcome in outcomes:
        if "wins!" in outcome:
            results_dict["win"] += 1
        elif "Push" in outcome:
            results_dict["push"] += 1
        else:
            results_dict["loss"] += 1

    # Update the total number of hands played
    results_dict["total_hands"] += hands_in_deal

def test_agents(num_deals=100):
    """
    Runs a series of games between the PIMC agent and the Basic Strategy agent,
    tracking their performance statistics.
    """
    # Initialize statistics dictionaries for both agents
    pimc_results = {"win": 0, "loss": 0, "push": 0, "total_hands": 0, "total_splits": 0}
    bs_results   = {"win": 0, "loss": 0, "push": 0, "total_hands": 0, "total_splits": 0}

    for i in range(1, num_deals + 1):
        # Run a game for each agent and update their stats
        parse_results(run_pimc_game(), pimc_results)
        parse_results(run_basic_strategy_game(), bs_results)
        
        # Print intermediate progress every 10 deals
        if i % 10 == 0:
            print(f"\n--- Completed {i}/{num_deals} Deals ---")
            print(f"PIMC -> Hands: {pimc_results['total_hands']} | Splits: {pimc_results['total_splits']} | Wins: {pimc_results['win']}")
            print(f"Basic Strategy -> Hands: {bs_results['total_hands']} | Splits: {bs_results['total_splits']} | Wins: {bs_results['win']}")

    def print_summary(agent_name, stats):
        """
        Prints a final summary of an agent's performance.
        """
        print(f"\n--- {agent_name} Performance Summary ---")
        print(f"Deals Played: {num_deals}")
        print(f"Total Hands Played: {stats['total_hands']}")
        print(f"Total Splits: {stats['total_splits']}")
        print(f"Wins: {stats['win']}, Losses: {stats['loss']}, Pushes: {stats['push']}")
        if stats['total_hands'] > 0:
            win_rate = (stats['win'] / stats['total_hands']) * 100
            print(f"Win Rate per Hand: {win_rate:.2f}%")
        else:
            print("No hands played.")

    # Print final performance summaries
    print_summary("PIMC Agent", pimc_results)
    print_summary("Basic Strategy Agent", bs_results)

# Run the simulation if this script is executed directly
if __name__ == "__main__":
    test_agents(num_deals=5000)