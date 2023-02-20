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
        self.moveFunctions = {'R':self.RookMoves,'p' : self.PawnMoves,'N' : self.KnightMoves, 'B' : self.BishopMoves, 'Q' : self.QueenMoves, 'K' : self.KingMoves}
    
    def makeMove(self, move):
        #won't work on pawn promotion, en passant and castling
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


    # all moves including checks

    def getValidMoves(self):
        return self.getAllPossible()

    # all moves without check

    def getAllPossible(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                colourturn = self.board[r][c][0]
                if (colourturn == "w" and self.whiteToMove) or (colourturn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) # calls the move function
        return moves

    def PawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--": #one pawn up 
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # two pawn up
                    moves.append(Move((r,c),(r-2,c), self.board))
            if c - 1 >= 0: # left capture
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c-1), self.board))
            if c+1 <= 7: #right capture
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1), self.board))
        else: # black movement
            if self.board[r+1][c] == "--": # one pawn down
                moves.append(Move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c), self.board))
            if c - 1 >= 0 :
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1), self.board))
            if c + 1 <= 7: 
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1, c+1), self.board))

    def RookMoves(self, r, c, moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1)) # different locations in tuple
        enemyColour = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i  #fixed from c to r 
                if 0 <= endrow <8 and 0 <= endcol < 8: # make sure it's on board
                    endpiece = self.board[endrow][endcol]
                    if endpiece == "--":
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                    elif endpiece[0] == enemyColour:
                        moves.append(Move((r,c),(endrow, endcol), self.board))
                        break
                    else:
                        break
                else:
                    break
           
    def KnightMoves(self, r, c, moves):
        pass
    
    def QueenMoves(self, r, c, moves):
        pass

    def KingMoves(self, r, c, moves):
        pass

    def BishopMoves(self, r, c, moves):
        pass

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
        self.moveID = self.startrow * 1000 + self.startcol * 100 + self.endrow * 10 + self.endcol
        print(self.moveID)

    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def ChessNotation(self):
        return self.getRankFile(self.startrow, self.startcol) + self.getRankFile(self.endrow, self.endcol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
