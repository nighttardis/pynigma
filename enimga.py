from string import ascii_lowercase


class Enimga:

    ROTERS = {
        'I':   {'letters': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'rotate': 'Q'},
        'II':  {'letters': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'rotate': 'E'},
        'III': {'letters': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'rotate': 'V'},
        'IV': {'letters': 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'rotate': 'J'},
        'V': {'letters': 'VZBRGITYUPSDNHLXAWMJQOFECK', 'rotate': 'Z'},
        'VI': {'letters': 'JPGVOUMFYQBENHZRDKASXLICTW', 'rotate': 'Z+M'},
        'VII': {'letters': 'NZJHGRCXMYSWBOUFAIVLPEKQDT', 'rotate': 'Z+M'},
        'VIII': {'letters': 'FKQHTLXOCBJSPDZRAMEWNIUYGV', 'rotate': 'Z+M'},
        'IC': {'letters': 'DMTWSILRUYQNKFEJCAZBPGXOHV', 'rotate': 'Q'},
        'IIC': {'letters': 'HQZGPJTMOBLNCIFDYAWVEUSRKX', 'rotate': 'E'},
        'IIIC': {'letters': 'UQNTLSZFMREHDPXKIBVYGJCWOA', 'rotate': 'V'},
        'RKT-I': {'letters': 'JGDQOXUSCAMIFRVTPNEWKBLZYH', 'rotate': 'Q'},
        'RKT-II': {'letters': 'NTZPSFBOKMWRCJDIVLAEYUXHGQ', 'rotate': 'E'},
        'RKT-III': {'letters': 'JVIUBHTCDYAKEQZPOSGXNRMWFL', 'rotate': 'V'},
        'RKT-UKW': {'letters': 'QYHOGNECVPUZTFDJAXWMKISRBL', 'rotate': 'Z'},
        'RKT-ETW': {'letters': 'QWERTZUIOASDFGHJKPYXCVBNML', 'rotate': 'Z'},
        'I-K': {'letters': 'PEZUOHXSCVFMTBGLRINQJWAYDK', 'rotate': 'Q'},
        'II-K': {'letters': 'ZOUESYDKFWPCIQXHMVBLGNJRAT', 'rotate': 'E'},
        'III-K': {'letters': 'EHRVXGAOBQUSIMZFLYNWKTPDJC', 'rotate': 'V'},
        'UKW-K': {'letters': 'IMETCGFRAYSQBZXWLHKDVUPOJN', 'rotate': 'Z'},
        'ETW-K': {'letters': 'QWERTZUIOASDFGHJKPYXCVBNML', 'rotate': 'Z'},
        'BETA': {'letters': 'LEYJVCNIXWPBQMDRTAKZGFUHOS', 'rotate': 'Z'},
        'GAMMA': {'letters': 'FSOKANUERHMBTIYCWLQPZXVGJD', 'rotate': 'Z'},
        'ETW': {'letters': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'rotate': 'Z'}
    }

    REFLECTORS = {
        'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
        'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
        'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
        'B Thin': 'ENKQAUYWJICOPBLMDXZVFTHRGS',
        'C Thin': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'
    }

    ALPHA = list(ascii_lowercase)

    def __init__(self, left='I', leftstart='a', leftringsetting='a',
                 center='II', centerstart='a', centerringsetting='a',
                 right='III', rightstart='a', rightringsetting='a',
                 reflector='B', steckerbrett: dict = None):
        """
        Build an enimga machine

        :param left: Roter key from ROTER for left Roter
        :param leftstart: Starting character for the left roter
        :param leftringsetting: change how the letter is encoded leaving the roter for the left roter
        :param center: Roter key from ROTER for center Roter
        :param centerstart: Starting character for the center roter
        :param centerringsetting: change how the letter is encoded leaving the roter for the center roter
        :param right: Roter key from ROTER for right Roter
        :param rightstart: Starting character for the right roter
        :param rightringsetting: change how the letter is encoded leaving the roter for the right roter
        :param reflector: reflector out of REFLECTORS keys
        :param steckerbrett: Steckerbrett dictionary of map of characters
        """
        self.steckerbrett = {k: k for k in self.ALPHA}
        if steckerbrett is not None:
            self.__validate_steckerbrett(steckerbrett=steckerbrett)

        if reflector not in self.REFLECTORS:
            raise ValueError('reflector is invalid')

        self.left_roter = None
        self.center_roter = None
        self.right_roter = None

        self.reset_roters(left=left, leftstart=leftstart, leftringsetting=leftringsetting,
                          center=center, centerstart=centerstart, centerringsetting=centerringsetting,
                          right=right, rightstart=rightstart, rightringsetting=rightringsetting)

        self.reflector = [letter.lower() for letter in self.REFLECTORS[reflector]]

    def __validate_steckerbrett(self, steckerbrett: dict, full_alpha: bool = False):
        """
        Validate the steckerbrett

        :param steckerbrett: Dictionary of mapping characters
        :param full_alpha: Boolean if the provided dictionary has all alpha characters
        :return:
        """
        alpha_set = set(self.ALPHA)
        steckerbrett_key_set = set(k.lower() for k in steckerbrett.keys())
        steckerbrett_value_set = set(k.lower() for k in steckerbrett.values())
        if not steckerbrett_key_set.issubset(alpha_set):
            raise ValueError(f"Steckerbrett keys incorrect unknown {steckerbrett_key_set - alpha_set}")
        if not steckerbrett_value_set.issubset(alpha_set):
            raise ValueError(f"Steckerbrett values incorrect unknown {steckerbrett_value_set - alpha_set}")
        if full_alpha:
            self.steckerbrett = steckerbrett
        else:
            for k, v in steckerbrett.items():
                if k in steckerbrett_value_set:
                    raise ValueError(f"Steckerbrett key also in values {k}, this isn't allowed")
                self.steckerbrett[k] = v
                self.steckerbrett[v] = k

    def update_roters(self):
        """
        Update the roters as the letter is being passed through the first pass

        :return:
        """

        # Split handles roters that have multiple rotation letters
        center_rotate = self.center_roter['rotate'].split('+')
        right_rotate = self.right_roter['rotate'].split('+')

        if self.ALPHA[self.center_roter['rotations'] % 26] in center_rotate:
            self.left_roter['rotations'] += 1
            self.center_roter['rotations'] += 1
        if self.ALPHA[self.right_roter['rotations'] % 26] in right_rotate:
            self.center_roter['rotations'] += 1
        self.right_roter['rotations'] += 1

    def rotate(self, roter: dict, letter: chr) -> chr:
        """
        Calculate the "encoded" value of the provided letter by the roter

        :param roter: Roter to run the letter through
        :param letter: letter to encode
        :return: encoded letter
        """
        temp = roter['rotations'] - roter['ringsetting']
        return self.ALPHA[
            (self.ALPHA.index(roter['letters'][(self.ALPHA.index(letter) + temp) % 26]) - temp) % 26]

    def rerotate(self, roter: dict, letter: chr) -> chr:
        """
        Encode letter as it is returning back through the roters

        :param roter: Roter to run the letter through
        :param letter: letter to encode
        :return: encoded letter
        """
        temp = roter['rotations'] - roter['ringsetting']
        return self.ALPHA[
            (self.ALPHA.index(roter['rletters'][(self.ALPHA.index(letter) + temp) % 26]) - temp) % 26]

    def encrypt(self, message: str) -> str:
        """
        Take a string/character and encode it

        :param message: what to encode
        :return: encoded message
        """
        encrypted_text = []
        for letter in message.split():
            for letter1 in letter.lower():
                self.update_roters()
                letter1 = self.steckerbrett[letter1]
                encrypted_letter = self.rotate(roter=self.right_roter, letter=letter1)
                encrypted_letter = self.rotate(roter=self.center_roter, letter=encrypted_letter)
                encrypted_letter = self.rotate(roter=self.left_roter, letter=encrypted_letter)
                encrypted_letter = self.reflector[self.ALPHA.index(encrypted_letter)].lower()
                encrypted_letter = self.rerotate(roter=self.left_roter, letter=encrypted_letter)
                encrypted_letter = self.rerotate(roter=self.center_roter, letter=encrypted_letter)
                encrypted_letter = self.rerotate(roter=self.right_roter, letter=encrypted_letter)
                encrypted_letter = self.steckerbrett[encrypted_letter]
                encrypted_text.append(encrypted_letter)
            encrypted_text.append(' ')
        return ''.join(encrypted_text)

    def get_roter_status(self) -> tuple:
        """
        Get the current status (current letter in window) of the roters

        :return: Tuple of roter status (Right, Center, Left) as looking at the machine
        """
        return (self.ALPHA[(self.right_roter['rotations'] - self.right_roter['ringsetting']) % 26],
                self.ALPHA[(self.center_roter['rotations'] - self.center_roter['ringsetting']) % 26],
                self.ALPHA[(self.left_roter['rotations'] - self.left_roter['ringsetting']) % 26])

    def get_roter_settings(self) -> tuple:
        """
        Get current settings (which roter, starting position, ring settings) for each roter

        :return: Tuple of roter esettings (Right, Center, Left) as looking at the machine
        """
        return ((self.right_roter['roter'], self.right_roter['start'], self.ALPHA[self.right_roter['ringsetting']]),
                (self.center_roter['roter'], self.center_roter['start'], self.ALPHA[self.center_roter['ringsetting']]),
                (self.left_roter['roter'], self.left_roter['start'], self.ALPHA[self.left_roter['ringsetting']]))

    def get_valid_roters(self) -> list:
        """
        Get the list of roters coded

        :return: List of valid roters
        """
        return list(self.ROTERS.keys())

    def get_steckerbrett(self) -> dict:
        """
        Get the current state of the steckerbrett

        :return: Streckerbrett Dictionary
        """
        return self.steckerbrett

    def __set_roters(self, roter: chr, start: chr, ringsetting: chr) -> dict:
        """
        Set invidual roter

        :param roter: which roter from ROTERS to use
        :param start: which starting letter to use
        :param ringsetting: change how the letter is encoded leaving the roter
        :return: Dictionary of settings
        """
        current_roter = {"letters": [letter.lower() for letter in self.ROTERS[roter]['letters']],
                         "rotations": self.ALPHA.index(start),
                         "rotate": self.ROTERS[roter]['rotate'].lower(),
                         "ringsetting": self.ALPHA.index(ringsetting), "roter": roter, "start": start}
        current_roter['rletters'] = [k for k, v in sorted(dict(zip(self.ALPHA, current_roter['letters'])).items(),
                                                          key=lambda item: item[1])]
        return current_roter

    def reset_roters(self, left: str = None, leftstart: str = None, leftringsetting: str = None,
                     center: str = None, centerstart: str = None, centerringsetting: str = None,
                     right: str = None, rightstart: str = None, rightringsetting: str = None):
        """
        Updates roters if changes are made after the machine is created,
         will use the current settings if nothing is provided

        :param left: Roter key from ROTER for left Roter
        :param leftstart: Starting character for the left roter
        :param leftringsetting: change how the letter is encoded leaving the roter for the left roter
        :param center: Roter key from ROTER for center Roter
        :param centerstart: Starting character for the center roter
        :param centerringsetting: change how the letter is encoded leaving the roter for the center roter
        :param right: Roter key from ROTER for right Roter
        :param rightstart: Starting character for the right roter
        :param rightringsetting: change how the letter is encoded leaving the roter for the right roter
        :return:
        """
        if self.left_roter is not None or self.center_roter is not None or self.right_roter is not None:
            tmp = self.get_roter_settings()

        if self.left_roter is not None:
            if left is None:
                left = tmp[2][0]
            if leftstart is None:
                leftstart = tmp[2][1]
            if leftringsetting is None:
                leftringsetting = tmp[2][2]

        if self.center_roter is not None:
            if center is None:
                center = tmp[1][0]
            if centerstart is None:
                centerstart = tmp[1][1]
            if centerringsetting is None:
                centerringsetting = tmp[1][2]

        if self.right_roter is not None:
            if right is None:
                right = tmp[0][0]
            if rightstart is None:
                rightstart = tmp[0][1]
            if rightringsetting is None:
                rightringsetting = tmp[0][2]

        if left not in self.ROTERS:
            raise ValueError('left Roter is invalid')
        if leftstart not in self.ALPHA:
            raise ValueError('leftstart isn\'t valid alpha')
        if leftringsetting not in self.ALPHA:
            raise ValueError('leftringsetting isn\'t valid alpha')
        if center not in self.ROTERS:
            raise ValueError('Center Roter is invalid')
        if centerstart not in self.ALPHA:
            raise ValueError('centerstart isn\'t valid alpha')
        if centerringsetting not in self.ALPHA:
            raise ValueError('centerringsetting isn\'t valid alpha')
        if right not in self.ROTERS:
            raise ValueError('Right Roter is invalid')
        if rightstart not in self.ALPHA:
            raise ValueError('rightstart isn\'t valid alpha')
        if rightringsetting not in self.ALPHA:
            raise ValueError('rightringsetting isn\'t valid alpha')

        self.right_roter = self.__set_roters(roter=right, start=rightstart, ringsetting=rightringsetting)

        self.center_roter = self.__set_roters(roter=center, start=centerstart, ringsetting=centerringsetting)

        self.left_roter = self.__set_roters(roter=left, start=leftstart, ringsetting=leftringsetting)

    def update_steckerbrett(self, steckerbrett: dict, full_alpha: bool = False):
        """
        Updates the steckerbrett after the machine is created

        :param steckerbrett: Dictionary of character maps
        :param full_alpha: Boolean if the provided steckerbrett has all alpha characters
        :return:
        """
        self.__validate_steckerbrett(steckerbrett=steckerbrett, full_alpha=full_alpha)
        self.reset_roters()


if __name__ == "__main__":
    a = Enimga()
    #A = a.encrypt("hello welcome to the world")
    # A = a.encrypt("aaaaa")
    # A = a.encrypt("AAAAA AAAAA AAAAA AAAAA AAA")
    A = a.encrypt("AAAAA AAAAA AAAAA")
    print(A)
    #b = Enimga()
    #B = b.encrypt(A)
    #print(B)
