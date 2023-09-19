from game import *
from room import *


def test() -> bool:
    
    test = Game()
    
    try:
        test.intro()
    except:
        return False

    try:
        test.run()
    except:
        return False

    return True
    
