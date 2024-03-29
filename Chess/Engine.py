import pygame
from pygame import mixer
move_piece = mixer.Sound('move_piece.wav')

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

        self.moveFunctions = {'R':self.RookMoves,'p' : self.PawnMoves,'N' : self.KnightMoves, 'B' : self.BishopMoves, 'Q' : self.QueenMoves, 'K' : self.KingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKinglocation = (7 , 4)
        self.blackKinglocation = (0 , 4)
        self.checkMate = False
        self.stalemate = False
        self.enpassantPossible = () #square where we can capture on with en passant.
        self.currentCastlingRights = CastleRights(True,True,True,True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]
# changed from currentcastlingrights 


    def makeMove(self, move):
        #won't work on pawn promotion, en passant and castling
        if self.board[move.startrow][move.startcol] != "--":
        #
            self.board[move.startrow][move.startcol] = "--"
            self.board[move.endrow][move.endcol] = move.piecemove
            self.moveLog.append(move) # records the moves for undo if wanted.
            self.whiteToMove = not self.whiteToMove # swap players
            #king loc. update
            if move.piecemove == 'wK':
                self.whiteKinglocation = (move.endrow, move.endcol)
            elif move.piecemove == 'bK':
                self.blackKinglocation = (move.endrow, move.endcol)    

            # pawn promotion
            if move.isPawnPromoted:
                self.board[move.endrow][move.endcol] = move.piecemove[0] + 'Q'
            #en passant
            if move.isEnpassantMove:
                self.board[move.startrow][move.endcol] = '--'

            if move.piecemove[1] == 'p' and abs(move.startrow - move.endrow) == 2:
                self.enpassantPossible = ((move.startrow + move.endrow)//2, move.startcol)  
            else:
                self.enpassantPossible = ()

            #castle move
            if move.iscastlemove:
                if move.endcol - move.startcol == 2: # kingside
                    self.board[move.endrow][move.endcol-1] = self.board[move.endrow][move.endcol+1] # moves the rook
                    self.board[move.endrow][move.endcol+1] = '--' # get rid of old rook
                    
                else:
                    self.board[move.endrow][move.endcol+1] = self.board[move.endrow][move.endcol-2]
                    self.board[move.endrow][move.endcol-2] = '--'

            #update castle rights
            self.updateCastleRights(move)
            self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))

    # undo the last move
    def undolastmove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            #moves moved piece back to the old square from pop function
            self.board[move.startrow][move.startcol] = move.piecemove
            #moves the captured piece back (if any)
            self.board[move.endrow][move.endcol] = move.piececaptured
            self.whiteToMove = not self.whiteToMove # once reversed must switch turns.
            #king loc.
            if move.piecemove == 'wK':
                self.whiteKinglocation = (move.startrow, move.startcol)
            elif move.piecemove == 'bK':
                self.blackKinglocation = (move.startrow, move.startcol) 
            #undo en passant
            if move.isEnpassantMove:
                self.board[move.endrow][move.endcol] = '--' 
                self.board[move.startrow][move.endcol] = move.piececaptured
                self.enpassantPossible = (move.endrow, move.endcol)

            if move.piecemove[1] == 'p' and abs(move.startrow - move.endrow) == 2:
                self.enpassantPossible = ()
    # all moves including checks
            self.castleRightsLog.pop() # get rid of castle rights
            self.currentCastlingRights = self.castleRightsLog[-1] # set to last in list
            #undo the castling move
            if move.iscastlemove:
                if move.endcol - move.startcol == 2: # kingside
                    self.board[move.endrow][move.endcol+1] = self.board[move.endrow][move.endcol-1]
                    self.board[move.endrow][move.endcol-1] = '--'
                else: # queenside
                    self.board[move.endrow][move.endcol-2] = self.board[move.endrow][move.endcol+1]
                    self.board[move.endrow][move.endcol+1] == '--'

    #update castle right
    def updateCastleRights(self,move):
        if move.piecemove == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.piecemove == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.piecemove == 'wR':
            if move.startrow == 7:
                if move.startcol == 0: # left rook
                    self.currentCastlingRights.wqs = False
                elif move.startcol == 7: # right rook
                    self.currentCastlingRights.wks = False
        elif move.piecemove == 'bR':
            if move.startrow == 0:
                if move.startcol == 0: # left rook
                    self.currentCastlingRights.bqs = False
                elif move.startcol == 7: # right rook
                    self.currentCastlingRights.bks = False

        #fixes empty square castling
        if move.piececaptured == 'wR':
            if move.endrow == 7:
                if move.endcol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endcol == 7:
                    self.currentCastlingRights.wks = False
        elif move.piececaptured == 'bR':
            if move.endrow == 0:
                if move.endcol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endcol == 7:
                    self.currentCastlingRights.bks = False



    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempcastlerights = CastleRights(self.currentCastlingRights.wks,
                                        self.currentCastlingRights.bks,self.currentCastlingRights.wqs,self.currentCastlingRights.bqs)#copy currents
        moves = self.getAllPossible()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKinglocation[0],self.whiteKinglocation[1], moves)
        else:
            self.getCastleMoves(self.blackKinglocation[0],self.blackKinglocation[1], moves)
        for i in range(len(moves)-1,-1,-1): # backward
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck(): 
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undolastmove()
        if len(moves)== 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.stalemate = True
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRights = tempcastlerights
        return moves

    # all moves without check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareAttacked(self.whiteKinglocation[0], self.whiteKinglocation[1])
        else:
            return self.squareAttacked(self.blackKinglocation[0],self.blackKinglocation[1])

    def squareAttacked(self , r , c):
        self.whiteToMove = not self.whiteToMove
        enemyMove = self.getAllPossible()
        self.whiteToMove = not self.whiteToMove 
        for move in enemyMove:
            if move.endrow == r and move.endcol == c: #sq under attack
                return True
        return False

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
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1), self.board, enpassantPossible=True))

            if c+1 <= 7: #right capture
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c+1), self.board, enpassantPossible=True))
        else: # black movement
            if self.board[r+1][c] == "--": # one pawn down
                moves.append(Move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c), self.board))
            if c - 1 >= 0 :
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c-1), self.board, enpassantPossible=True))
            if c + 1 <= 7: 
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c+1), self.board, enpassantPossible=True))

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
        knightmoves = ((-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(-1,2),(1,2),(1,-2))
        enemyColour = "b" if self.whiteToMove else "w"
        for m in knightmoves:
            endrow = r + m[0]
            endcol = c + m[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] == enemyColour or endpiece == "--":
                    moves.append(Move((r,c),(endrow,endcol), self.board))
                    move_piece.play()

    def QueenMoves(self, r, c, moves):
        self.RookMoves(r,c,moves)
        self.BishopMoves(r,c,moves)


    def KingMoves(self, r, c, moves):
        directions = ((-1,-1),(-1,1),(1,1),(1,-1),(-1,0),(1,0),(0,-1),(0,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endrow = r + directions[i][0]
            endcol = c + directions[i][1]
            if 0<= endrow < 8 and 0 <= endcol <8:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] != allyColor or endpiece == "--":
                    moves.append(Move((r,c),(endrow,endcol), self.board))
        


    def BishopMoves(self, r, c, moves):
        direction = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColour = "b" if self.whiteToMove else "w"
        for d in direction:
            for i in range(1,8):
                endrow = r+d[0] * i
                endcol = c+d[1] * i 
                if 0 <= endrow < 8 and 0 <= endcol < 8:
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
                
    def getCastleMoves(self, r, c, moves):
        #if self.inCheck():
        if self.squareAttacked(r,c):
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(r,c,moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(r,c,moves)

    def getKingsideCastleMoves(self, r, c, moves,):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareAttacked(r,c+1) and not self.squareAttacked(r, c+2):
                moves.append(Move((r,c),(r,c+2), self.board, iscastlemove=True))

    def getQueensideCastleMoves(self, r, c, moves ):
        print("QUEEN")
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareAttacked(r,c-1) and not self.squareAttacked(r, c-2):
                moves.append(Move((r,c),(r,c-2), self.board, iscastlemove=True))
                
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():
    #making chess notation using dictionaries.

    ranksToRows = {"1" : 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" :7}
    colsToFiles = {v : k for k, v in filesToCols.items()}

    def __init__(self, start_sg, end_sg, board, enpassantPossible = False, iscastlemove = False):
        self.startrow = start_sg[0]
        self.startcol = start_sg[1]
        self.endrow = end_sg[0]
        self.endcol = end_sg[1]
        self.piecemove = board[self.startrow][self.startcol]
        self.piececaptured = board[self.endrow][self.endcol]
        self.isPawnPromoted = (self.piecemove == "wp" and self.endrow == 0) or (self.piecemove == "bp" and self.endrow == 7) 

        #en passant
        self.isEnpassantMove = enpassantPossible
        if self.isEnpassantMove:
            self.piececaptured = 'wp' if self.piecemove == 'bp' else 'bp'

        #castle
        self.iscastlemove = iscastlemove


        
       


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
