#Import Functions
import time
from server_req import player_join_req, hit, check_status
from receiver import receiver

class laser_tag_hardware:

    rec: receiver
    participating: bool
    game_status: int

    ID = 33 # Hardcoded

    def __init__(self):
        self.rec = receiver(self.join, self.get_hit)
        self.participating = False
        self.game_status = 0

    def join(self):
        if not self.participating:
            if player_join_req(self.ID) == 0:
                self.participating = True
                self.rec.activate_wand()
                self.rec.reset_life()

    def get_hit(self):
        if self.participating and self.game_status:
            hit()
            self.rec.decrease_life()
            if self.rec.life == 0:
                self.participating = False
                self.rec.disable_wand()

    def get_status(self):
        self.game_status = check_status()
        if self.game_status == 0:
            self.participating = False

    def blink_led(self):
        self.rec.reset_life()
        time.sleep(0.1)
        for i in range(0,3):
            if self.participating:
                self.rec.reset_life()
                return

            self.rec.decrease_life()
            time.sleep(0.1)

    def activate(self):

        # General game flow 

        while( True ):

            if not self.participating:
                self.blink_led()
            else:
                self.get_status()
                time.sleep(2)
        
def main():
    game = laser_tag_hardware()
    game.activate()

if __name__ == '__main__':
    main()
    
        
        
    
    
    
    
    

    





        



