package ahu.ewn.game.initial;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import ahu.ewn.board.ChessBoard;
import ahu.ewn.board.Piece;
import ahu.ewn.board.Piece_Type;

/**
 * 随机布局策略，六个棋子随机放置
 *
 */
public class RandomInit extends InitStrategy {

    /**
     * 构造函数
     */
    public RandomInit() {
        super();
        setLabel("随机布局");
    }

    @Override
    public ChessBoard getBoard(Piece_Type myTurn) {
        // TODO 自动生成的方法存根
        ChessBoard board = new ChessBoard();

        List<Byte> Pieces = new ArrayList<Byte>();
        Pieces.add(Piece.createprice_id(myTurn, (byte) 1));
        Pieces.add(Piece.createprice_id(myTurn, (byte) 2));
        Pieces.add(Piece.createprice_id(myTurn, (byte) 3));
        Pieces.add(Piece.createprice_id(myTurn, (byte) 4));
        Pieces.add(Piece.createprice_id(myTurn, (byte) 5));
        Pieces.add(Piece.createprice_id(myTurn, (byte) 6));

        if (myTurn == Piece_Type.RED) {
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3 - i; j++) {
                    int index = new Random().nextInt(Pieces.size());
                    board.setPiece(Pieces.get(index), i, j);
                    Pieces.remove(index);
                }
            }
        } else {
            for (int i = 4; i >= 2; i--) {
                for (int j = 4; j >=6-i ; j--) {
                    int index = new Random().nextInt(Pieces.size());
                    board.setPiece(Pieces.get(index), i, j);
                    Pieces.remove(index);
                }
            }

        }

        return board;
    }

}
