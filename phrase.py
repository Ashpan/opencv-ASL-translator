class phrase():
    word = ""
    phrase = ""
    
    def __init__(self):
        super().__init__()
    
    def endPhrase(self):
        self.phrase += self.word + " "
        self.word = ""

    def addLetter(self, letters):
        if(self.word == ""):
            

    
