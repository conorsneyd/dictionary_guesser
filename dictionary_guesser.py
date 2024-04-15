from random import randrange
from choose_random_entry import choose_random_entry

class Player:
    def __init__(self, number):
        self.name = "Player " + str(number)
        self.number = number
        self.score = 0
     
def introduction():
    #Print instructions when user first runs program
    print("""\nWelcome to Dictionary Guesser!
          
How to play:
          
Choose a number of players (recommended: 1 - 4) and a number of rounds (recommended: 3).

In each round, each player will be shown a definition and have to guess the word it refers to.

If you guess the word correctly, you'll earn up to one point per letter in the word.

If you guess the word incorrectly, any correct letters will be revealed.

If you're stuck, you can get a hint to reveal a letter. 

For every hint and incorrect guess, you'll lose one potential point.

If the number of potential points reaches 0 or you choose to skip the word, your turn will be over and you won't get any points for that round.
          
At the end of the last round, the player with the most points wins!
          """)
    ready_to_begin = input("\nEnter \"b\" to begin.\n")
    while ready_to_begin.lower() != "b":
        ready_to_begin = input("\n\nEnter \"b\" to begin.\n")
    start_game()

def start_game():
    #get number of players and rounds from input
    players = {}
    all_words_guessed = []
    num_players_input = input("\nHow many players are there?\n")
    num_players = validate_number(num_players_input)
    for i in range(1, num_players + 1):
        #create a Player object for each player and add to players dictionary (starting with "Player 1")
        players[i] = Player(i)
    rounds_input = input("\nHow many rounds would you like to play? (1 - 10)\n")
    rounds = validate_number(rounds_input)
    current_player_number = 1
    play_round(current_player_number, rounds, rounds, num_players, players, all_words_guessed)

def validate_number(number):
    #make sure input is an integer - get new input if not
    try:
        return int(number)
    except:
        number = input("Please enter a number\n")
        return validate_number(number)
    
def play_round(current_player_number, rounds, rounds_remaining, num_players, players, all_words_guessed):
    #play a round (each player gets one turn per round)
    if rounds_remaining > 0:
        print(f"\nRound {rounds - rounds_remaining + 1}!")
        play_turn(current_player_number, rounds, rounds_remaining, num_players, players, all_words_guessed)
    else:
        game_over(current_player_number, num_players, players, all_words_guessed)

def play_turn(current_player_number, rounds, rounds_remaining, num_players, players, all_words_guessed):
    #play an individual player's turn
    current_player = players[current_player_number]
    hints_given = 0
    incorrect_guesses = 0
    #get a random word from the dictionary and convert letters to list of _'s
    word, definition, part_of_speech = get_word(current_player, all_words_guessed)
    letters = ["_" for letter in range(len(word))]
    turn_over = False
        
    if num_players > 1:
        print(f"\n{current_player.name}'s turn.")
    print("\nGuess the word...")
    print(f"\nDefinition: {definition} ({part_of_speech}) ({len(word)} letters)")
    print(letters)

    while turn_over == False:
        #respond to player input until turn is over
        turn_score = get_score(word, hints_given, incorrect_guesses)
        print(f"\nPoints remaining for this word: {turn_score}")
        guess = input("\nEnter your guess (or enter \"get hint\" to get a hint or \"skip word\" to skip this word)\n")
        while len(guess) != len(word) and guess != "get hint" and guess != "skip word":
            guess = input(f"\nPlease enter {len(word)} letters (or enter \"get hint\" to get a hint or \"skip word\" to skip this word):\n")
        if guess.lower() == word.lower():
            #if guess is correct, assign points and end turn
            turn_over = True
            current_player.score += turn_score
            print("\nCorrect!")
            if turn_score == 1:
                print (f"\nYou scored 1 point this round. Your total score is {current_player.score}.")
            else:
                print(f"\nYou scored {turn_score} points this round. Your total score is {current_player.score}.")
        elif guess == "get hint":
            #give user hint by revealing a letter (as long as this wouldn't reduce the turn's potential points to 0)
            if not "_" in letters:
                print("\nNo more hints available! (All letters have already been revealed)")
            elif turn_score <= 1:
                print("\nNo more hints available! (Only 1 point remaining for this word)")
            else:
                hints_given += 1
                letters = hint(word, letters)
                print(letters)
        elif guess == "skip word":
            #skip word to end turn with 0 points
            turn_over = True
            print(f"\nThe word was {word}.")
            print(f"\nYou scored 0 points this round. Your total score is {current_player.score}.\n")
        else:
            #if guess is incorrect, reveal any correct letters
            incorrect_guesses += 1
            turn_score = get_score(word, hints_given, incorrect_guesses)
            if turn_score > 0:
                print("\nWrong! Try again.")
                for i in range(len(guess)):
                    if guess[i] == word[i]:
                        letters[i] = word[i]
                print(letters)

        if turn_score == 0:
            #end turn (and reveal word) if potential points reaches 0
            print(f"\nWrong! No points remaining for this word.\n\nThe word was \"{word}\".")
            print(f"\nYou scored 0 points this round. Your total score is {current_player.score}.\n")
            turn_over = True

    all_words_guessed.append(word)

    if num_players > 1 and current_player_number < num_players:
        #if multiple players and current player not last player, move on to next player's turn within current round
        current_player_number += 1
        play_turn(current_player_number, rounds, rounds_remaining, num_players, players, all_words_guessed)
    else:
        #else move on to next round (print scores at end of round if multiple players)
        if num_players > 1 and rounds_remaining > 1:
            print("\nRound over.\n")
            print_scores("current", players)
        current_player_number = 1
        play_round(current_player_number, rounds, rounds_remaining - 1, num_players, players, all_words_guessed)

def get_word(current_player, all_words_guessed):
    #choose a random word from the dictionary and make sure it's longer than one letter and hasn't already been guessed in this game
    word, definition, part_of_speech = choose_random_entry()
    if word in all_words_guessed or len(word) <= 1:
        return get_word(current_player)
    else:
        return word, definition, part_of_speech

def print_scores(current_or_final, players):
    #print current or final scores for all players
    for player in players:
                print(f"{players[player].name}'s {current_or_final} score is {players[player].score}.")        

def game_over(current_player_number, num_players, players, all_words_guessed):
        current_player = players[current_player_number]
        print("\nGame over!\n")
        if num_players > 1:
            #choose winner(s) if multiple players and print score
            winner = []
            print_scores("final", players)
            for player in players:
                if not winner or players[player].score > players[winner[0]].score:
                    winner = [player]
                elif players[player].score == players[winner[0]].score:
                    winner.append(player)
            if len(winner) == 1:
                print(f"\n{players[winner[0]].name} wins!")
            else:
                winner_string = f"\nIt's a tie! Players {str(players[winner[0]].number)}"
                for i in range(1, len(winner) - 1):
                    winner_string += (", " + (str(players[winner[i]].number)))
                winner_string += (f" and {str(players[winner[-1]].number)} win!\n") 
                print(winner_string)
        else:
            #print score if only one player
            print(f"\nYour final score is {current_player.score}.\n")
        
        #allow user to start another game
        play_again = input("\nWould you like to play another game? (y/n)\n")
        while play_again.lower() not in ["y", "n"]:
            play_again = input("Please enter y or n:\n")
        if play_again.lower() == "y":
            start_game()

def get_score(word, hints_given, incorrect_guesses):
    #calculate score for current turn
    score = len(word) - hints_given - incorrect_guesses
    if score <= 0:
        return 0
    return score

def hint(word, letters):
    #reveal a random leter in the word (option not available if all letters already revealed - prevents infinite loop)
    hint_given = False
    while hint_given == False:
        i = randrange(len(letters))
        if letters[i] == "_":
            letters[i] = word[i]
            hint_given = True
    return letters
    

introduction()