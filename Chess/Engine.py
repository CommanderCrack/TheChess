class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.whiteToMove = True
        self.moveLog = []
    def makeMove(self, move):
        #won't work on pawn promotion, en passant and castling
        # annotate this on word:
        if self.board[move.startrow][move.startcol] != "--":
        #
            self.board[move.startrow][move.startcol] = "--"
            self.board[move.endrow][move.endcol] = move.piecemove
            self.moveLog.append(move) # records the moves for undo if wanted.
            self.whiteToMove = not self.whiteToMove # swap players
    
    # undo the last move
    def undolastmove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            #moves moved piece back to the old square from pop function
            self.board[move.startrow][move.startcol] = move.piecemove
            #moves the captured piece back (if any)
            self.board[move.endrow][move.endcol] = move.piececaptured
            self.whiteToMove = not self.whiteToMove # once reversed must switch turns.

class Move():
    #making chess notation using dictionaries.

    ranksToRows = {"1" : 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" :7}
    colsToFiles = {v : k for k, v in filesToCols.items()}

    def __init__(self, start_sg, end_sg, board):
        self.startrow = start_sg[0]
        self.startcol = start_sg[1]
        self.endrow = end_sg[0]
        self.endcol = end_sg[1]
        self.piecemove = board[self.startrow][self.startcol]
        self.piececaptured = board[self.endrow][self.endcol]

    def ChessNotation(self):
        return self.getRankFile(self.startrow, self.startcol) + self.getRankFile(self.endrow, self.endcol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
