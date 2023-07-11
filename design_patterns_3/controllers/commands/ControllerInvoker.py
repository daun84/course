from controllers.commands.interfaces.ICommand import ICommand

class ControllerInvoker:
    __instance = None

    @staticmethod
    def instance():
        if ControllerInvoker.__instance is None:
            ControllerInvoker.__instance = ControllerInvoker()
        return ControllerInvoker.__instance

    def __init__(self):
        if ControllerInvoker.__instance is not None:
            raise Exception("Only one instance of ControllerInvoker allowed")
        ControllerInvoker.__instance = self
        self.undo_stack: List[ICommand] = []
        self.redo_stack: List[ICommand] = []

    def clear_history(self):
        self.undo_stack = []
        self.redo_stack = []

    def execute_command(self, command: ICommand):
        self.undo_stack.append(command)
        command.execute()
        self.redo_stack = []

    def undo_command(self):
        if len(self.undo_stack):
            command = self.undo_stack.pop() # stack type of behavior last element
            self.redo_stack.append(command)
            command.undo()

    def redo_command(self):
        if len(self.redo_stack):
            command = self.redo_stack.pop()
            self.undo_stack.append(command)
            command.execute()