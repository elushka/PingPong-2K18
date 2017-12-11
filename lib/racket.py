import sprobj

class Racket(sprobj.SprObj):

    def get_hit_effect(self):
        if self.y:
            return self.y * -1