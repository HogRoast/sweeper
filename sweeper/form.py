class Form:
    played = 0
    won = 0
    drawn = 0
    lost = 0
    glfor = 0
    glagn = 0
    gldif = 0
    points = 0
   
    def asList(self):
        return [self.played, self.won, self.drawn, self.lost, \
                self.glfor, self.glagn, self.gldif, self.points]

