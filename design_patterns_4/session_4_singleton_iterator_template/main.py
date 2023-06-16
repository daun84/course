import random
from views.WindowMain import WindowMain
import time

random.seed(time.time())
windowMain = WindowMain.instance()
windowMain.show()