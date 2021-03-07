import os


class phrase():
    word = ""
    phrase = ""
    fileLocation = os.path.dirname(os.path.realpath(__file__))
    f = open(fileLocation + '\\dictionary.txt', 'r')
    dictionary = f.read().split('\n')
    f.close()

    def __init__(self):
        super().__init__()

# move string from word to phrase and reset word
    def endWord(self):
        if(self.word != ""):
            self.phrase += self.word + " "
            self.word = ""
            print("ending word")

# add letter to word variable
    def addLetter(self, letters):
        if(len(letters[0][0]) > 1):
            if(self.word == ""):
                self.word = letters[0][0]
            else:
                self.word = " " + letters[0][0]
            self.endWord()
        elif(self.word == ""):
            self.word += (letters[0][0]).lower()
        else:
            for i in letters:
                if [x for x in self.dictionary if x.startswith(self.word+i[0].lower())] != []:
                    self.word += i[0].lower()
                    break

# return the phrase
    def getPhrase(self):
        return (self.phrase + self.word)
    def reset(self):
        self.word = ""
        self.phrase = ""