class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bC","bQ","bK","bB","bN","bS"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wS"]]
        self.whiteToMove = True
        self.moveLog = []