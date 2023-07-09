class PlayerProfile:
    def __init__(self, data):
        self.name = data['name']
        self.id = data['ID']
        self.score = data['score']
        self.matches = data['game']
        self.win = data['win']
        self.lose = data['lose']
        self.role = ""
        
    def updateMatch(self, match):
        self.match += match
        return self.match
    
    def updateWin(self):
        self.win += 1
        
    def updateLose(self):
        self.lose += 1
        
    def updateScore(self, score):
        self.score += score
        
    def updateRole(self, role):
        self.role = role
        
    def getInfo(self):
        return {
            "name" : self.name,
            "data" : {
                "name" : self.name,
                "ID" : self.id,
                "score" : self.score,
                "game" : self.matches,
                "win" : self.win,
                "lose" : self.lose
            }
        }
        