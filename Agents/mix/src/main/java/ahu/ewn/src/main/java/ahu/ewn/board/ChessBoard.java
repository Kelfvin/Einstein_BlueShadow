package ahu.ewn.board;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import ahu.ewn.game.Move;
import ahu.ewn.game.MoveDirection;


//这个类只是来布局棋盘的
/**
 * 棋盘类。以byte型5x5数组表示棋盘，存储棋子ID号（详见ahu.ewn.board.Piece类）。
 */
public class ChessBoard {


    //参数与构造函数

    /**
     * 棋盘大小（行数/列数）
     */
    public static final short SIZE = 5;

    /**
     * 二维byte类型数组表示的棋盘,存储棋子ID
     */
    private byte[][] board;

    /**
     * 蓝方在场的棋子数量(定义此属性只为加快isWin()执行速度)
     */
    private byte pieceNumber_blue = 0;

    /**
     * 红方在场的棋子数量(定义此属性只为加快isWin()执行速度)
     */
    private byte pieceNumber_red = 0;

    public Object player;

    /**
     * 构造空的棋盘对象
     */
    public ChessBoard() {
        pieceNumber_blue = 0;
        pieceNumber_red = 0;
        board = new byte[SIZE][SIZE];
        for (int i = 0; i < SIZE; i++) {
            Arrays.fill(board[i], (byte) 0);
        }
    }


    //函数方法

    /**
     * 将指定棋子放置于指定棋位上
     *
     * @param id  棋子ID
     * @param row 行号
     * @param col 列号
     */
    public void setPiece(byte id, int row, int col) {
        this.board[row][col] = id;
        if (Piece.getType(id) == Piece_Type.BLUE) pieceNumber_blue++;
        else if (Piece.getType(id) == Piece_Type.RED) pieceNumber_red++;
    }

    /**
     * 获取指定棋位上的棋子
     *
     * @param row 行号
     * @param col 列号
     * @return Piece 棋子
     */
    public byte getPiece(int row, int col) {
        return this.board[row][col];
    }

    /**
     * 获取指定棋子的棋位
     *
     * @param piece_id 棋子
     * @return int[2]数组  res[0]为行号，res[1]为列号
     */
    public int[] getLocation(byte piece_id) {
        int[] row_col=new int[2];
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (board[i][j] == piece_id) {
                    row_col[0] = i;
                    row_col[1] = j;
                    return row_col;
                }
            }
        }
        return row_col;
    }

    /**
     * 获取棋盘数组
     *
     * @return byte[5][5] board
     */
    public byte[][] getBoard() {
        return this.board;
    }

    /**
     * 获取红方在场棋子个数
     *
     * @return int 红方在场棋子数
     */
    public int getPieceNumber_RED() {
        return this.pieceNumber_red;
    }

    /**
     * 获取蓝方在场棋子个数
     *
     * @return int 蓝方在场棋子数
     */
    public int getPieceNumber_BLUE() {
        return this.pieceNumber_blue;
    }

    /**
     * 获取当前棋盘类型为type的棋子数（暂时用不到）
     *
     * @param type 棋子类型
     * @return int
     */
    public int getPieceCount(Piece_Type type) {
        if (type == Piece_Type.BLUE) return getPieceNumber_BLUE();
        else if (type == Piece_Type.RED) return getPieceNumber_RED();
        else return 25 - getPieceNumber_BLUE() - getPieceNumber_RED();
    }

    /**
     * 根据指定骰子点数获取符合游戏规则的可移动的棋子
     * @param type 棋子类型
     * @param dice 骰子
     * @return List 棋子id列表
     */
    public List<Byte> getPiecesByDice(Piece_Type type, byte dice) {
        List<Byte> GoPrice = new ArrayList<Byte>(2);//最多两个棋子
        byte[] Pieces = new byte[7]; //分别记录1-6的棋子是否存在（1/0）
        Arrays.fill(Pieces, (byte) 0);
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (Piece.getType(board[i][j]) == type)
                    Pieces[Piece.getNumber(board[i][j])] = 1;
            }
        }
        //点数棋子存在则只能移动此棋子
        if (Pieces[dice] == 1) {
            GoPrice.add(Piece.createprice_id(type, dice));
        } else {
            //不存在则可以移动它的上一个或下一个棋子
            for (byte i = (byte) (dice + 1); i < 7; i++) {
                if (Pieces[i] == 1) {
                    GoPrice.add(Piece.createprice_id(type, i));
                    break;
                }
            }
            for (byte i = (byte) (dice - 1); i > 0; i--) {
                if (Pieces[i] == 1) {
                    GoPrice.add(Piece.createprice_id(type, i));
                    break;
                }
            }
        }
        return GoPrice;
    }

    /**
     * 获取指定一方的所有在场棋子
     *
     * @param type 棋子类型
     * @return List 玩家type在场的所有棋子
     */
    public List<Byte> getPieces(Piece_Type type) {
        List<Byte> Pieces = new ArrayList<Byte>(6);//最多为6
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (Piece.getType(board[i][j]) == type) Pieces.add(board[i][j]);
            }
        }

        return Pieces;
    }

    /**
     * 根据指定的棋子，求能使该棋子移动的骰子点数；若该棋子不在棋盘上，返回空。
     *
     * @param piece_id 棋子ID
     * @return 返回能使该棋子移动的骰子点数集合。若该棋子不在棋盘上，返回空。
     */
    public List<Byte> getDicesByPiece(byte piece_id) {
        List<Byte> Dices = new ArrayList<Byte>(6);
        byte pieceNumber = Piece.getNumber(piece_id);

        byte[] Pieces = new byte[7];
       for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (Piece.getType(board[i][j]) == Piece.getType(piece_id))
                    Pieces[Piece.getNumber(board[i][j])] = 1;
            }
        }

        //若该棋子不在棋盘上，返回空集
        if (Pieces[pieceNumber] == 0) return Dices;

        Dices.add(pieceNumber);

        for (int i = pieceNumber + 1; i < 7 && Pieces[i] == 0; i++) {
            Dices.add((byte) i);
        }

        for (int i = pieceNumber - 1; i > 0 && Pieces[i] == 0; i--) {
            Dices.add((byte) i);
        }
        return Dices;
    }

    /**
     * 处理走子动作，更新棋盘，返回处理结果(被吃棋子id、0、不可行-1)
     *
     * @param move 动作
     * @return 若有棋子被吃，返回被吃的棋子id；若无棋子被吃，返回0；若棋子位置越界，返回-1
     */
    public byte pieceMove(Move move) {
        byte piece_id = move.getPiece_id();
        MoveDirection direction = move.getDirection();
        int[] location_old = getLocation(piece_id);
        int[] location_new = getLocation(piece_id);

        if (Piece.getType(piece_id) == Piece_Type.BLUE) {
            if (direction == MoveDirection.FORWARD) {
                location_new[0]--;
                location_new[1]--;
            } else if (direction == MoveDirection.LEFT) {
                location_new[1]--;
            } else {
                location_new[0]--;
            }
        } else {
            if (direction == MoveDirection.FORWARD) {
                location_new[0]++;
                location_new[1]++;
            } else if (direction == MoveDirection.LEFT) {
                location_new[1]++;
            } else {
                location_new[0]++;
            }
        }

        if (location_new[0] >= SIZE || location_new[0] < 0 || location_new[1] >= SIZE || location_new[1] < 0) {
            return -1;
        }

        board[location_old[0]][location_old[1]] = 0;
        byte id = board[location_new[0]][location_new[1]];
        board[location_new[0]][location_new[1]] = piece_id;

        if (Piece.getType(id) == Piece_Type.BLUE) pieceNumber_blue--;
        else if (Piece.getType(id) == Piece_Type.RED) pieceNumber_red--;

        return id;
    }

    /**
     * 判断某方是否获胜
     * @param turn 一方
     * @return boolean 是否获胜
     */
    public final boolean isWin(Piece_Type turn) {
        if(turn == Piece_Type.BLUE){
            if (Piece.getType(getPiece(0, 0)) == Piece_Type.BLUE) return true;
            if (pieceNumber_red == 0) return true;
        }
        else{
            if (Piece.getType(getPiece(4, 4)) == Piece_Type.RED) return true;
            if (pieceNumber_blue == 0) return true;
        }
        return false;
    }

    /**
     * 判断游戏是否结束
     *
     * @return boolean 游戏结束返回true；没有结束返回false
     */
    public final boolean isEnd(){
        return isWin(Piece_Type.BLUE) || isWin(Piece_Type.RED);
    }

    /**
     * 获取获胜方
     * @return PieceType 获胜方。如果游戏没有结束，返回PieceType.NULL
     */
    public final Piece_Type getWinner(){
        if(isWin(Piece_Type.RED)) return Piece_Type.RED;
        if(isWin(Piece_Type.BLUE)) return Piece_Type.BLUE;
        return Piece_Type.NULL;
    }

    /**
     * 移除指定坐标的棋子(用不到)
     *
     * @param row 行号
     * @param col 列号
     */
    public void removePiece(int row, int col) {
        byte id = board[row][col];
        board[row][col] = 0;

        if (Piece.getType(id) == Piece_Type.BLUE) pieceNumber_blue--;
        else if (Piece.getType(id) == Piece_Type.RED) pieceNumber_red--;
    }

    /**
     * 打印至控制台（调试函数）
     *
     * @param tabNum 每行之前的Tab数量
     */
    // public void printBoard(int tabNum) {
    //     for (int i = 0; i < SIZE; i++) {
    //         for (int j = 0; j < SIZE; j++) {
    //             for (int k = 0; k < tabNum; k++) System.out.print("	");
    //             System.out.print(Piece.toString(this.board[i][j]) + "	");
    //         }
    //         System.out.println();
    //     }
    // }

    /*
     * 在调试和System.out.println(board)时使用，可以直接打印棋盘对象
     */
    @Override
    public String toString() {
        StringBuilder string = new StringBuilder();
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                string.append(Piece.toString(board[i][j]));
            }
            if (i != 4) string.append("\n");
        }
        return string.toString();
    }

    public void show(){
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                System.out.print(board[i][j]+" ");
            }
            if (i != 4) System.out.println();;
        }
        System.out.println();
    }
    /**
     * 清空棋盘
     */
    public void clear() {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                board[i][j] = 0;
            }
        }
        pieceNumber_red = 0;
        pieceNumber_blue = 0;
    }

    /*
     * 克隆一个新的棋盘对象
     */
    @Override
    public ChessBoard clone() {
        ChessBoard newBoard = new ChessBoard();
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                newBoard.board[i][j] = this.board[i][j];
            }
        }
        newBoard.pieceNumber_blue = this.pieceNumber_blue;
        newBoard.pieceNumber_red = this.pieceNumber_red;
        return newBoard;
    }

    /**
     * 判断本棋盘是否与指定棋盘相同
     *
     * @param board 被比较的棋盘
     * @return true  相同<br>
     * false 不同
     */
    public boolean compareTo(ChessBoard board) {
        // TODO 自动生成的方法存根
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (this.board[i][j] != board.board[i][j]) return false;
            }
        }
        return true;
    }
    @Override
    public boolean equals(Object object) {
        ChessBoard board = (ChessBoard) object;
        return this.compareTo(board);
    }

   

}
