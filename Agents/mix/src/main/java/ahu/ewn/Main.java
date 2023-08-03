package ahu.ewn;


import ahu.ewn.board.ChessBoard;
import ahu.ewn.board.Piece;
import ahu.ewn.board.Piece_Type;
import ahu.ewn.game.Game;
import ahu.ewn.game.Move;
import ahu.ewn.game.MoveDirection;
import ahu.ewn.game.Player;
import ahu.ewn.game.initial.StaticInit;
import ahu.ewn.strategy.move.metekaluo.Mengtekaluo;

/**
 * 程序测试，比界面中的自动对弈快很多
 *
 */
public class Main {

    public static void main(String[] args) {
        int[][] board = {{-3,-2,-1,0,0},
                         {-4,-5,0,0,0},
                         {-6,0,0,0,4},
                         {0,0,0,1,2},
                         {0,0,3,5,6}};

        
        int[] resultData = entry(board,(byte)3, 1);
        for (int resultData2 : resultData) {
            System.out.print(resultData2+" ");
        }
        System.out.println("");
    }

    public static int[] entry(int[][] board, byte randInteger, int color ) {
        Piece_Type firstPlayer = null;

        if(color == 1){
            firstPlayer = Piece_Type.BLUE;
        }
        else if(color == -1){
            firstPlayer = Piece_Type.RED;
        }

    ChessBoard redBoard=new ChessBoard();
    ChessBoard blueBoard=new ChessBoard();
    for(int i=0; i < board.length; i++){
        for(int j=0; j < board[i].length; j++){
            if(board[i][j] < 0){
            redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte)(-board[i][j])), i, j);
            }
            else if(board[i][j] > 0){
            blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte)board[i][j]),i,j);
            }
        }
    }
        
        // redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 2), 0, 1);
        // redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 3), 2, 0);
        // redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 4), 0, 2);
        // redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 5), 1, 1);
        // redBoard.setPiece(Piece.createprice_id(Piece_Type.RED, (byte) 6), 0, 0);

    
        // blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 1), 3, 4);
        // blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 2), 4, 3);
        // blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 3), 2, 4);
        // blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 4), 4, 2);
        // blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 5), 3, 3);
        // blueBoard.setPiece(Piece.createprice_id(Piece_Type.BLUE, (byte) 6), 4, 4);
      
        
        // 指定蓝方的布局策略和下棋策略
        Player bluePlayer = new Player(Piece_Type.BLUE, new StaticInit(blueBoard,redBoard), new Mengtekaluo());
        // 指定红方的布局策略和下棋策略
        Player redPlayer = new Player(Piece_Type.RED, new StaticInit(blueBoard,redBoard), new Mengtekaluo());

        // 定义一局游戏，并设置玩家为上面定义的玩家
        Game game = new Game();
        game.setPlayer(bluePlayer);
        game.setPlayer(redPlayer);

        //获得一个
        //重置游戏，生成初始布局
        game.reset(firstPlayer);
        
        // 随机生成一个骰子点数
        byte dice = randInteger;


        // 行棋方的走子策略产生一个合法走法
        Move move = game.getNowPlayer().getMoveStrategy().getMove(game, dice);

        System.out.println(game.getNowPlayer().getTurn());
        // 得到起点坐标
        int[] startPoint = getPosition(move.getPiece_id(), board);
        int[] endPoint = new int[2];

       if(firstPlayer == Piece_Type.RED){
         if(move.getDirection() == MoveDirection.FORWARD){
            endPoint[0] = startPoint[0]+1;
            endPoint[1] = startPoint[1]+1;
         }
         else if(move.getDirection() == MoveDirection.LEFT){
            endPoint[0] = startPoint[0]+1;
            endPoint[1] = startPoint[1];
         }
         else{
            endPoint[0] = startPoint[0];
            endPoint[1] = startPoint[1]+1;
         }
       }
       
       if(firstPlayer == Piece_Type.BLUE){
        if(move.getDirection() == MoveDirection.FORWARD){
            endPoint[0] = startPoint[0]-1;
            endPoint[1] = startPoint[1]-1;
         }
         else if(move.getDirection() == MoveDirection.LEFT){
            endPoint[0] = startPoint[0]-1;
            endPoint[1] = startPoint[1];
         }
         else{
            endPoint[0] = startPoint[0];
            endPoint[1] = startPoint[1]-1;
         }
       }

       int[] returnPoints = new int[4];
       returnPoints[0] = startPoint[0];
       returnPoints[1] = startPoint[1];
       returnPoints[2] = endPoint[0];
       returnPoints[3] = endPoint[1];
       return returnPoints;
        
     }

     static int[] getPosition(byte id, int[][] board){
        System.out.println(id);
        int[] position = new int[2];
        //这是棋子上对应的号
        int code = 0;

        if(id<20 && id > 10){
            code = id-10;
        }
        else if(id > 20){
            code = -(id-20);
        }
        
        for(int i=0; i<board.length; i++){
            for(int j=0; j < board.length; j++){
                if(code == board[i][j]){
                    position[0] = i;
                    position[1] = j;
                }
            }
        }
        return position;
     }
    
    
     
 
}


