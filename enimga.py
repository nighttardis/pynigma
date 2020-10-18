from string import ascii_lowercase


class Enimga:

    ROTERS = {
        'I':   {'letters': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'rotate': 'Q'},
        'II':  {'letters': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'rotate': 'E'},
        'III': {'letters': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'rotate': 'V'}
    }

    REFLECTORS = {
        'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
        'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
        'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
        'B Thin': 'ENKQAUYWJICOPBLMDXZVFTHRGS',
        'C Thin': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'
    }

    ALPHA = list(ascii_lowercase)

    # ROTERS = {
    #     'IC': 'DMTWSILRUYQNKFEJCAZBPGXOHV',
    #     'IIC': 'HQZGPJTMOBLNCIFDYAWVEUSRKX',
    #     'IIIC': 'UQNTLSZFMREHDPXKIBVYGJCWOA',
    #     'RKT-I': 'JGDQOXUSCAMIFRVTPNEWKBLZYH',
    #     'RKT-II': 'NTZPSFBOKMWRCJDIVLAEYUXHGQ',
    #     'RKT-III': 'JVIUBHTCDYAKEQZPOSGXNRMWFL',
    #     'RKT-UKW': 'QYHOGNECVPUZTFDJAXWMKISRBL',
    #     'RKT-ETW': 'QWERTZUIOASDFGHJKPYXCVBNML',
    #     'I-K': 'PEZUOHXSCVFMTBGLRINQJWAYDK',
    #     'II-K': 'ZOUESYDKFWPCIQXHMVBLGNJRAT',
    #     'III-K': 'EHRVXGAOBQUSIMZFLYNWKTPDJC',
    #     'UKW-K': 'IMETCGFRAYSQBZXWLHKDVUPOJN',
    #     'ETW-K': 'QWERTZUIOASDFGHJKPYXCVBNML',
    #     'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
    #     'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
    #     'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
    #     'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
    #     'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
    #     'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
    #     'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
    #     'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
    #     'Beta': 'LEYJVCNIXWPBQMDRTAKZGFUHOS',
    #     'Gamma': 'FSOKANUERHMBTIYCWLQPZXVGJD',
    #     'Reflector A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
    #     'Reflector B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
    #     'Reflector C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
    #     'Reflector B Thin': 'ENKQAUYWJICOPBLMDXZVFTHRGS',
    #     'Reflector C Thin': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ',
    #     'ETW': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # }

    def __init__(self, left='I', leftstart='a', leftringsetting='a',
                 center='II', centerstart='a', centerringsetting='a',
                 right='III', rightstart='a', rightringsetting='a',
                 reflector='B', steckerbrett: dict = None):

        self.steckerbrett = {k: k for k in self.ALPHA}
        if steckerbrett is not None:
            self.__validate_steckerbrett(steckerbrett=steckerbrett)

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
        if reflector not in self.REFLECTORS:
            raise ValueError('reflector is invalid')

        self.right_roter = {"letters": [letter.lower() for letter in self.ROTERS[right]['letters']],
                            "rotations": self.ALPHA.index(rightstart), "rotate": self.ROTERS[right]['rotate'].lower(),
                            "ringsetting": self.ALPHA.index(rightringsetting), "roter": right, "start": rightstart}
        self.right_roter['rletters'] = [k for k, v in sorted(dict(zip(self.ALPHA, self.right_roter['letters'])).items(),
                                                             key=lambda item: item[1])]

        self.center_roter = {"letters": [letter.lower() for letter in self.ROTERS[center]['letters']],
                             "rotations": self.ALPHA.index(centerstart), "rotate": self.ROTERS[center]['rotate'].lower(),
                             "ringsetting": self.ALPHA.index(centerringsetting), "roter": center, "start": centerstart}
        self.center_roter['rletters'] = [k for k, v in
                                         sorted(dict(zip(self.ALPHA, self.center_roter['letters'])).items(),
                                                key=lambda item: item[1])]

        self.left_roter = {"letters": [letter.lower() for letter in self.ROTERS[left]['letters']],
                           "rotations": self.ALPHA.index(leftstart), "rotate": self.ROTERS[left]['rotate'].lower(),
                           "ringsetting": self.ALPHA.index(leftringsetting), "roter": left, "start": leftstart}
        self.left_roter['rletters'] = [k for k, v in sorted(dict(zip(self.ALPHA, self.left_roter['letters'])).items(),
                                                            key=lambda item: item[1])]

        self.reflector = [letter.lower() for letter in self.REFLECTORS[reflector]]

    def __validate_steckerbrett(self, steckerbrett: dict):
        alpha_set = set(self.ALPHA)
        steckerbrett_key_set = set(k.lower() for k in steckerbrett.keys())
        steckerbrett_value_set = set(k.lower() for k in steckerbrett.values())
        if not steckerbrett_key_set.issubset(alpha_set):
            raise ValueError(f"Steckerbrett keys incorrect unknown {steckerbrett_key_set - alpha_set}")
        if not steckerbrett_value_set.issubset(alpha_set):
            raise ValueError(f"Steckerbrett values incorrect unknown {steckerbrett_value_set - alpha_set}")
        for k, v in steckerbrett.items():
            if k in steckerbrett_value_set:
                raise ValueError(f"Steckerbrett key also in values {k}, this isn't allowed")
            self.steckerbrett[k] = v
            self.steckerbrett[v] = k


    def update_roters(self):
        if self.ALPHA[self.center_roter['rotations'] % 26] == self.center_roter['rotate']:
            self.left_roter['rotations'] += 1
            self.right_roter['rotations'] += 1
        if self.ALPHA[self.right_roter['rotations'] % 26] == self.right_roter['rotate']:
            self.center_roter['rotations'] += 1
        self.right_roter['rotations'] += 1

    def rotate(self, roter, letter):
        temp = roter['rotations'] - roter['ringsetting']
        return self.ALPHA[
            (self.ALPHA.index(roter['letters'][(self.ALPHA.index(letter) + temp) % 26]) - temp) % 26]

    def rerotate(self, roter, letter):
        temp = roter['rotations'] - roter['ringsetting']
        return self.ALPHA[
            (self.ALPHA.index(roter['rletters'][(self.ALPHA.index(letter) + temp) % 26]) - temp) % 26]

    def encrypt(self, message):
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

    def get_roter_status(self):
        return (self.ALPHA[(self.right_roter['rotations'] - self.right_roter['ringsetting']) % 26],
                self.ALPHA[(self.center_roter['rotations'] - self.center_roter['ringsetting']) % 26],
                self.ALPHA[(self.left_roter['rotations'] - self.left_roter['ringsetting']) % 26])

    def get_roter_settings(self):
        return ((self.right_roter['roter'], self.right_roter['start'], self.ALPHA[self.right_roter['ringsetting']]),
                (self.center_roter['roter'], self.center_roter['start'], self.ALPHA[self.center_roter['ringsetting']]),
                (self.left_roter['roter'], self.left_roter['start'], self.ALPHA[self.left_roter['ringsetting']]))

    def get_valid_roters(self):
        return self.ROTERS.keys()


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
