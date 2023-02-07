import chess

class AIChess:
    def __init__(self):
        """
        Initialize the library by creating board: chess.Board which is the starting chess board in the chess library,
        it is public for you to use however be careful as you can break some functions and 
        minimaxDepth: int which is the depth of the search algorithm. 
        Higher the better but requires move computational power. Single process and needs to be > 1. Default 3.
        """
        self.board = chess.Board()
        self.minimaxDepth = 3

    def chessAIMove(self):
        """
        chessAIMove() -> List[str]
        Returns a list of the best possible legal_moves for whoevers turn it is in UCI however, 
        it is possible that one or more of the entries can be the string 'claim_draw' instead of a UCI 
        which is to indicate the desire to claim a draw like FIFTY_MOVES or THREEFOLD_REPETITION
        """
        bestMovesStr = []
        alpha = -50000
        beta = 50000
        if self.get_isWhiteTurn():
            bestMoveEval = -50000
            if self.board.copy().outcome(claim_draw = True) != None and (str(self.board.copy().outcome(claim_draw = True).termination) != 'Termination.CHECKMATE' or str(self.board.copy().outcome(claim_draw = True).termination) != 'Termination.VARIANT_WIN' or str(self.board.copy().outcome(claim_draw = True).termination) != 'Termination.VARIANT_LOSS'):
                bestMoveEval = 200
                alpha = 200
                bestMovesStr.append('claim_draw')
            for child in reversed(list(self.board.legal_moves)):
                newGameBoard = self.board.copy()
                newGameBoard.push(child)
                eval = self.__minimax(self.minimaxDepth - 1, newGameBoard, alpha, beta, False)
                if eval == bestMoveEval:
                    bestMovesStr.append(str(newGameBoard.peek()))
                elif eval > bestMoveEval:
                    bestMovesStr.clear()
                    bestMovesStr.append(str(newGameBoard.peek()))
                    bestMoveEval = eval
                    alpha = eval
        else:
            bestMoveEval = 50000
            if self.board.copy().outcome(claim_draw = True) != None and (str(self.board.copy().outcome(claim_draw = True).termination) != 'Termination.CHECKMATE' or str(self.board.copy().outcome(claim_draw = True).termination) != 'Termination.VARIANT_WIN' or str(self.board.copy().outcome(claim_draw = True).termination) != 'Termination.VARIANT_LOSS'):
                bestMoveEval = -200
                beta = -200
                bestMovesStr.append('claim_draw')
            for child in reversed(list(self.board.legal_moves)):
                newGameBoard = self.board.copy()
                newGameBoard.push(child)
                eval = self.__minimax(self.minimaxDepth - 1, newGameBoard, alpha, beta, True)
                if eval == bestMoveEval:
                    bestMovesStr.append(str(newGameBoard.peek()))
                elif eval < bestMoveEval:
                    bestMovesStr.clear()
                    bestMovesStr.append(str(newGameBoard.peek()))
                    bestMoveEval = eval
                    beta = eval
        return bestMovesStr

    def __minimax(self, depth: int, game: chess.Board, alpha: int, beta: int, isMaximisingPlayer: bool):
        if game.outcome() != None:
            if str(game.outcome().termination) == 'Termination.CHECKMATE' or str(game.outcome().termination) == 'Termination.VARIANT_WIN' or str(game.outcome().termination) == 'Termination.VARIANT_LOSS':
                if game.outcome().winner == chess.WHITE:
                    return 1000
                else:
                    return -1000
            else:
                if self.minimaxDepth - depth % 2 == 0:
                    return 200
                else:
                    return -200
        elif depth == 0:
            return self.get_whiteBlackPointsDifference(game)

        if isMaximisingPlayer:
            maxEval = -50000
            if game.copy().outcome(claim_draw = True) != None and (str(game.copy().outcome(claim_draw = True).termination) != 'Termination.CHECKMATE' or str(self.board.copy().outcome(claim_draw = True).termination) != 'Termination.VARIANT_WIN' or str(game.copy().outcome(claim_draw = True).termination != 'Termination.VARIANT_LOSS')):
                if self.minimaxDepth - depth % 2 == 0:
                    maxEval = 200
                else:
                    maxEval = -200
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    return maxEval
            for child in reversed(list(game.legal_moves)):
                newGameBoard = game.copy()
                newGameBoard.push(child)
                eval = self.__minimax(depth - 1, newGameBoard, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    return maxEval
            return maxEval
        else:
            minEval = 50000
            if game.copy().outcome(claim_draw = True) != None and (str(game.copy().outcome(claim_draw = True).termination) != 'Termination.CHECKMATE' or str(self.board.copy().outcome(claim_draw = True).termination) != 'Termination.VARIANT_WIN' or str(game.copy().outcome(claim_draw = True).termination) != 'Termination.VARIANT_LOSS'):
                if self.minimaxDepth - depth % 2 == 0:
                    maxEval = -200
                else:
                    maxEval = 200
                beta = min(beta, minEval)
                if beta <= alpha:
                    return minEval
            for child in reversed(list(game.legal_moves)):
                newGameBoard = game.copy()
                newGameBoard.push(child)
                eval = self.__minimax(depth - 1, newGameBoard, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    return minEval
            return minEval

    def get_whiteBlackPointsDifference(self, game: chess.Board):
        """
        get_whiteBlackPointsDifference(game: chess.Board) -> int
        Returns the point difference between white and black
        where Pawn: 1, Bishop: 3, Knight: 3, Rook: 5, Queen 9
        """
        whitePoints = 0
        blackPoints = 0

        boardAs2DList = [['.' for i in range(8)] for j in range(8)]
        for square in chess.SQUARES:
            if game.piece_at(square) != None:
                boardAs2DList[int((63 - square) / 8)][square % 8] = game.piece_at(square).symbol()
        
        for boardAs2DListRow in boardAs2DList:
            for boardSquare in boardAs2DListRow:
                if boardSquare == 'P':
                    whitePoints += 1
                elif boardSquare == 'p':
                    blackPoints += 1
                elif boardSquare == 'B':
                    whitePoints += 3
                elif boardSquare == 'N':
                    whitePoints += 3
                elif boardSquare == 'R':
                    whitePoints += 5
                elif boardSquare == 'b':
                    blackPoints += 3
                elif boardSquare == 'n':
                    blackPoints += 3
                elif boardSquare == 'r':
                    blackPoints += 5
                elif boardSquare == 'Q':
                    whitePoints += 9
                elif boardSquare == 'q':
                    blackPoints += 9

        return whitePoints - blackPoints

    def makeChessMove(self, uci):
        """
        makeChessMove(uci: chess.Move | str) -> None
        Needs to be at least pseudo_legal
        """
        self.board.push_uci(str(uci))

    def listAllPossibleMoves(self):
        """
        listAllPossibleMoves() -> List[Move]
        Lists all possible legal_moves for whoevers turn it is for each piece
        """
        return list(self.board.legal_moves)

    def listUCIPosPossibleMoves(self, uciPos: str):
        """
        listUCIPosPossibleMoves(uciPos: str) -> List[Move]
        Lists all possible legal_moves for whoevers turn it is for the uciPos like 'a2', or 'b1'
        Returns an empty List if no possible moves
        """
        allPossibleMoves = self.listAllPossibleMoves()
        uciPossibleMoves = []
        for Move in allPossibleMoves:
            if Move.uci()[0:2] == uciPos:
                uciPossibleMoves.append(Move)
        return uciPossibleMoves

    def reset(self):
        """
        reset() -> None 
        Resets board in chess.Board
        """
        self.board.reset()

    def willMoveNeedPawnPromotion(self, uci):
        """
        willMoveNeedPawnPromotion(uci: chess.Move | str) -> bool
        Return True if move will result in a pawn promotion, False otherwise
        """
        if (str(uci)[1] == '2' and str(uci)[3] == '1' and self.board.piece_at(chess.parse_square(str(uci)[0:2])).symbol().upper() == 'P') or (str(uci)[1] == '7' and str(uci)[3] == '8' and self.board.piece_at(chess.parse_square(str(uci)[0:2])).symbol().upper() == 'P'):
            return True
        else:
            return False

    def pieceToPieceType(self, result):
        """
        pieceToPieceType(result: chess.Piece | str) -> int
        Return chess.PieceType as a int
        """
        if str(result).lower() == 'p':
            return 1
        elif str(result).lower() == 'n':
            return 2
        elif str(result).lower() == 'b':
            return 3
        elif str(result).lower() == 'r':
            return 4
        elif str(result).lower() == 'q':
            return 5
        elif str(result).lower() == 'k':
            return 6
        else:
            return 0

    def rowColToUCI(self, rowColFrom: list[int], rowColTo: list[int]):
        """
        rowColToUCI(rowColFrom: list[int], rowColTo: list[int]) -> str
        Accepts two List[int] which is the row and col from and to locations 
        Returns a str which is a uci representing the inputs
        """
        uciCol = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return uciCol[rowColFrom[1]] + str(8 - rowColFrom[0]) + uciCol[rowColTo[1]] + str(8 - rowColTo[0])

    def uciToRowCol(self, uci):
        """
        uciToRowCol(uci: chess.Move | str) -> List[int], List[int]
        Accepts a str which is a uci
        Returns two List[int] which are the row and col from and to representing the inputs
        """
        colUCI = dict(a = 0, b = 1, c = 2, d = 3, e = 4, f = 5, g = 6, h = 7)
        return [8 - int(str(uci)[1]), colUCI[str(uci)[0]]], [8 - int(str(uci)[3]), colUCI[str(uci)[2]]]

    def rowColToUCIPos(self, row: int, col: int):
        """
        rowColToUCIPos(row: int col: int) -> str
        Accepts a row and col of a 2D list that is the chess board
        Returns a uciPos which is a single position like a2 or b1 representing the inputs
        """
        uciCol = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return uciCol[col] + str(8 - row)

    def uciToRowColPos(self, uciPos: str):
        """
        uciToRowColPos(uciPos: str) -> int, int
        Accepts a uciPos which is a single position like a2 or b1 
        Returns a row and col of a 2D list that is the chess board representing the inputs
        """
        colUCI = dict(a = 0, b = 1, c = 2, d = 3, e = 4, f = 5, g = 6, h = 7)
        row = 8 - int(uciPos[1])
        col = colUCI[uciPos[0]]
        return row, col

    def uciToFlippedRowCol(self, uci):
        """
        uciToFlippedRowCol(uci: chess.Move | str) -> List[int], List[int]
        Accepts a uci
        Returns two List[int] hich are the row and col from and to in a 2D list that is the chess board representing the inputs but flipped so that white is on top and black is bottom
        """
        flippedRowColFrom, flippedRowColTo = self.uciToRowCol(uci)
        return self.flipRowCol(flippedRowColFrom, flippedRowColTo)

    def flippedRowColToUCIPos(self, row: int, col: int):
        """
        flippedRowColToUCIPos(row: int, col: int) -> str
        Accepts a row and col position that has been flipped so that white is on top and black is on bottom
        Returns a uciPos which is a single position like a2 or b1 representing the inputs
        """
        flippedRow, flippedCol = self.flipRowColPos(row, col)
        return self.rowColToUCIPos(flippedRow, flippedCol)

    def uciToFlippedRowColPos(self, uciPos: str):
        """
        uciToFlippedRowColPos(uciPos: str) -> int, int
        Accepts a uciPos which is a single position like a2 or b1 
        Returns a row and col position that has been flipped so that white is on top and black is on bottom representing the inputs
        """
        row, col = self.uciToRowColPos(uciPos)
        return self.flipRowColPos(row, col)

    def flipRowCol(self, rowColFrom: list[int], rowColTo: list[int]):
        """
        flipRowCol(rowColFrom: list[int], rowColTo: list[int]) -> List[int], List[int]
        Accepts two List[int] which is the row and col from and to locations 
        Returns two List[int] which is the row and col from and to locations but flipped so that white is one top and black is on bottom
        """
        rowColFrom[0] = 7 - rowColFrom[0]
        rowColFrom[1] = 7 - rowColFrom[1]
        rowColTo[0] = 7 - rowColTo[0]
        rowColTo[1] = 7 - rowColTo[1]
        return rowColFrom, rowColTo

    def flipRowColPos(self, row: int, col: int):
        """
        flipRowColPos(row: int, col: int) -> int, int
        Accepts two int which is the row and col for a location
        Returns two int which is the row and col for a location but flipped so that white is one top and black is on bottom
        """
        return 7 - row, 7 - col

    def get_boardAs2DList(self):
        """
        get_boardAs2DList() -> List[int][int]
        Returns a 2D list that represents the chess board with white on bottom and black on top for easy use 
        """
        boardAs2DList = [['.' for i in range(8)] for j in range(8)]
        for square in chess.SQUARES:
            if self.board.piece_at(square) != None:
                boardAs2DList[int((63 - square) / 8)][square % 8] = self.board.piece_at(square).symbol()
        return boardAs2DList

    def get_boardAs2DListFlipped(self):
        """
        get_boardAs2DListFlipped() -> List[int][int]
        Returns a 2D list that represents the chess board but flipped so white is on top and black is on bottom for easy use 
        """
        boardAs2DList = [['.' for i in range(8)] for j in range(8)]
        for square in chess.SQUARES:
            if self.board.piece_at(square) != None:
                boardAs2DList[int((square) / 8)][(63 - square) % 8] = self.board.piece_at(square).symbol()
        return boardAs2DList

    def get_isWhiteTurn(self):
        """
        get_isWhiteTurn() -> bool
        Returns a bool where True is if it is white's turn and False if it is black's turn
        """
        return self.board.turn

    def get_isStartOfGame(self):
        """
        get_isStartOfGame() -> bool
        Returns a bool where True is if it is the start of the game and False if it isn't
        """
        try:
            self.board.peek()
        except IndexError:
            return True
        return False
