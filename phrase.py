import os
class phrase():
    word = ""
    phrase = ""
    fileLocation = os.path.dirname(os.path.realpath(__file__))
    f = open(fileLocation + '\\dictionary.txt', 'r')
    dictionary = f.read().split('\n')

    def __init__(self):
        super().__init__()
    
    def endPhrase(self):
        self.phrase += self.word + " "
        self.word = ""

    def addLetter(self, letters):
        if(self.word == ""):
            word += (letters[0][0]).lower()
        else:
            for i in letters:
                if [x for x in dictionary if x.startswith(self.word+i(0).lower())] != []:
                    word += i(0).lower()
                    break
    def getPhrase(self):
        return (phrase+word)

    
