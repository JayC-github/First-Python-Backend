#pylint: disable=C0301, R0201
"""
This program specifies a class for the game hangman
"""
import textwrap
import random
import string as stringmod

ATTEMPTS_COUNT = 6
WORD_SOURCE = "words"

class Hangman:
    '''
    hangman class to simulate the game
    '''

    def __init__(self):
        """
        this function will initialize the game and set attempts and words

        input: none
        output: none
        """

        self.__attempts = ATTEMPTS_COUNT
        self.__guessletters = []
        self.__word = ""
        self.__active = False

    def game_start(self):
        """
        A function to start a game of hangman
        """
        self.__attempts = ATTEMPTS_COUNT
        self.__guessletters = []
        self.__word = self.get_word()
        self.__active = True

    def guess_letter(self, letter):
        """
        this function will check if the guess is valid given a letter
        if not valid it will reduce attempts until no more attempts left

        input: str letter
        output: str message
        """

        if isinstance(letter, str) and letter.lower() in stringmod.ascii_lowercase:
            msg = ""
            letter = letter.lower()
            if not letter in self.__guessletters:
                if letter in self.__word:
                    msg += "Good guess!\n"
                    self.__guessletters.append(letter)
                else:
                    msg += "Bad guess!\n"
                    self.__attempts -= 1

                msg += self.__display_letters()

                # when no more attempts are available
                if self.__attempts == 0:
                    msg += "YOU LOST\n"
                    msg += f"The correct word is: {self.__word}\n"
                    self.reset()
                elif all(elem in self.__guessletters for elem in self.__word):
                    msg += "Your guess is correct! YOU WIN\n"
                    self.reset()
            else:
                # letter has already been guessed
                msg += "Letter already guessed\n"
        else:
            return "Letter invalid\n"

        return msg

    def guess_word(self, word):
        """
        this function will check if the guess is correct given a word
        if not valid it will reduce attempts until no more attempts left

        input: str letter
        output: str message
        """

        if isinstance(word, str) and self.wordcheck(word.lower()):
            msg = ""
            if word.lower() == self.__word:
                msg += "Your guess is correct! YOU WIN\n"
                self.reset()
            else:
                self.__attempts -= 1
                msg += "Guessed wrong!\n"
                # display letters
                msg += self.__display_letters()

                if self.__attempts == 0:
                    msg += "YOU LOST\n"
                    msg += f"The correct word is: {self.__word}\n"
                    self.reset()
            return msg
        return "Word is invalid\n"

    def __display_letters(self):
        """
        this function will display the correctly guessed letters of the word

        input: none
        output: str message
        """
        msg = ""
        temp = ["_"] * len(self.__word)

        for idx, i in enumerate(self.__word, 0):
            if i in self.__guessletters:
                temp[idx] = i

        msg += self.__display_hangman()
        msg += ("".join(temp))
        msg += "\n"

        return msg

    def __gameend(self):
        """
        this function will display the word and reset the game

        input: none
        output: str message
        """

        msg = ("The word is {}!".format(self.__word))
        self.reset()

        return msg

    def reset(self):
        """
        this function will reinitialize all properties of the hangman class

        input: none
        output: none
        """
        self.game_start()

    def quit(self):
        """
        this function will stop the game and set its active status to false

        input: none
        output: none
        """

        self.reset()
        self.__active = False

    def isactive(self):
        """
        this function will check whether there is an active game or not

        input: none
        output: bool active
        """
        return self.__active

    def __display_hangman(self):
        """
        this function will return the ascii art of hangman where
        the art will depend on number of attempts left

        input: none
        output: str ascii_art
        """
        return self.ascii_art("""
    ______________
    | /          |
    |/           |
    |          {1}{0}{2}
    |            {3}
    |           {4}{5}
    |
    |
    |           
    |____________|""".format(' ' if self.__attempts >= 6  else 'O', '  ' if self.__attempts >= 5  else ' \\', ' ' if self.__attempts >= 4  else '/', ' ' if self.__attempts >= 3  else '|', '  ' if self.__attempts >= 2  else ' /', ' ' if self.__attempts >= 1  else '\\') + "\n")

    def get_word(self):
        """
        this function will get words from a given source file, filter out words that
        only have ascii characters and then convert them to lower case.
        from this lower case word list it will return a random value

        input: none
        output: str random word
        """
        word_file = WORD_SOURCE
        word_list = open(word_file).read().splitlines()
        ascii_lower_list = [word.lower() for word in word_list if self.wordcheck(word.lower())]

        return random.choice(ascii_lower_list)

    def ascii_art(self, string):
        """
        this function will modify the string in a format that is needed

        input: str string
        output: str wrappedstring
        """
        return textwrap.dedent(string)

    def wordcheck(self, word):
        '''
        Function to check if given word is a valid word in ascii lowercase

        input: str word
        output: bool true or false
        '''
        for letter in word:
            if letter not in stringmod.ascii_lowercase:
                return False
        return True

if __name__ == "__main__":
    GAME = Hangman()
    print(GAME.guess_letter("t"))
    print(GAME.guess_letter("r"))
    print(GAME.guess_letter("a"))
    print(GAME.guess_letter("t"))
    print(GAME.guess_letter("c"))
