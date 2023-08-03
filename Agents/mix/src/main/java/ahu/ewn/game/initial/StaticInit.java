package ahu.ewn.game.initial;

import java.util.HashMap;
import java.util.Map;

import ahu.ewn.board.ChessBoard;
import ahu.ewn.board.Piece;
import ahu.ewn.board.Piece_Type;

/**
 * 固定棋盘布局。默认情况下该策略将生成以下棋盘,因为该布局是别人统计的最优的布局方式<br>
 * [26 22 24 00 00]<br>
 * [21 25 00 00 00]<br>
 * [23 00 00 00 13]<br>
 * [00 00 00 15 11]<br>
 * [00 00 14 12 16]<br>
 * 除此之外，也可以指定一种棋盘布局
 */
public class StaticInit extends InitStrategy {

    /**
     * 指定的棋盘布局
     */
    private Map<Piece_Type, ChessBoard> boards;

    /**
     * 构造函数，生成默认布局
     */
    public StaticInit() {
        super();
        setLabel("固定布局");

        boards=new HashMap<Piece_Type, ChessBoard>();

        ChessBoard redBoard=new ChessBoard();
        redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 1), 1, 0);
        redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 2), 0, 1);
        redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 3), 2, 0);
        redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 4), 0, 2);
        redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 5), 1, 1);
        redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 6), 0, 0);

        ChessBoard blueBoard=new ChessBoard();
        blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 1), 3, 4);
        blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 2), 4, 3);
        blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 3), 2, 4);
        blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 4), 4, 2);
        blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 5), 3, 3);
        blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 6), 4, 4);

        boards.put(Piece_Type.BLUE, blueBoard);
        boards.put(Piece_Type.RED, redBoard);
    }

    /**
     * 构造函数，指定双方的布局
     * 
     * @param blueBoard 蓝方棋盘布局
     * @param redBoard 红方棋盘布局
     */
    public StaticInit(ChessBoard blueBoard, ChessBoard redBoard) {
        boards=new HashMap<Piece_Type, ChessBoard>();
        boards.put(Piece_Type.BLUE, blueBoard);
        boards.put(Piece_Type.RED, redBoard);
    }

    @Override
    public ChessBoard getBoard(Piece_Type myTurn) {
        // TODO 自动生成的方法存根
        return boards.get(myTurn);
    }

    /**
     * 设置某一方的布局
     * 
     * @param type 玩家
     * @param board 初始布局
     */
    public void setBoard(Piece_Type type, ChessBoard board) {
        boards.put(type, board);
    }
}
