if __name__ == "__main__":
    import tkinter as tk
    from block import Block
    from blockchain import Blockchain
    from gui import GUI

    root = tk.Tk()
    blockchain = Blockchain()
    gui = GUI(blockchain, root)

    root.mainloop()
