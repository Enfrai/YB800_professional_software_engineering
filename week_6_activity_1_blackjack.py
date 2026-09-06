import random

# Deck setup: unlimited deck, 10s for J/Q/K, 11 for Ace
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def deal_card():
    """Returns a random card from the deck."""
    return random.choice(cards)


def calculate_score(cards_list):
    """Calculates score and handles Blackjack and Ace adjustments."""
    # Check for Blackjack (Ace + 10-value card = 21)
    if sum(cards_list) == 21 and len(cards_list) == 2:
        return 0  # 0 represents Blackjack in this game logic

    # Handle Ace (11): convert 11 to 1 if score exceeds 21
    if 11 in cards_list and sum(cards_list) > 21:
        cards_list.remove(11)
        cards_list.append(1)

    return sum(cards_list)


def compare(user_score, computer_score):
    """Compares user and computer scores to decide the outcome."""
    if user_score == computer_score:
        return "Draw 🙃"
    elif computer_score == 0:
        return "Lose, opponent has Blackjack 😱"
    elif user_score == 0:
        return "Win with a Blackjack 😎"
    elif user_score > 21:
        return "You went over. You lose 😭"
    elif computer_score > 21:
        return "Opponent went over. You win 💥"
    elif user_score > computer_score:
        return "You win 😃"
    else:
        return "You lose 😤"


def play_game():
    user_cards = []
    computer_cards = []
    is_game_over = False

    # Deal initial 2 cards to user and computer
    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())

    # User turn loop
    while not is_game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)

        print(f" Your cards: {user_cards}, current score: {user_score}")
        print(f" Computer's first card: {computer_cards[0]}")

        if user_score == 0 or computer_score == 0 or user_score > 21:
            is_game_over = True
        else:
            should_deal = input("Type 'y' to get another card, type 'n' to pass: ").lower()
            if should_deal == 'y':
                user_cards.append(deal_card())
            else:
                is_game_over = True

    # Computer/Dealer turn loop (must draw if score is < 17)
    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    print("\n--- Final Results ---")
    print(f" Your final hand: {user_cards}, final score: {user_score}")
    print(f" Computer's final hand: {computer_cards}, final score: {computer_score}")
    print(compare(user_score, computer_score))


# Game Loop
if __name__ == "__main__":
    while input("\nDo you want to play a game of Blackjack? Type 'y' or 'n': ").lower() == 'y':
        print("\n" * 10)  # Clear space for new game
        play_game()