from view import View
from controller import Controller
from model import Game

def main():
    model = Game()
    controller = Controller(model)
    view = View(controller)
    view.main()

if __name__ == '__main__':
    main()