from src.gui.root import Root

class View:
    def __init__(self):
        self.root = Root()
        
        self.start_mainloop()

    def start_mainloop(self):
        self.root.mainloop()
