package ahu.ewn.game;

import ahu.ewn.board.Piece;

/**
 * 下棋动作。由棋子编码ID和移动方向决定。
 *
 */
public class Move {
    /**
     * 棋子
     */
    private byte piece_id;

    /**
     * 移动方向
     */
    private MoveDirection direction;

    /**
     * 构造函数
     *
     * @param piece_id 棋子ID
     * @param direction 移动方向
     */
    public Move(byte piece_id, MoveDirection direction) {
        this.piece_id = piece_id;
        this.direction = direction;
    }





    /**
     * 获取棋子
     *
     * @return Piece 棋子
     */
    public byte getPiece_id() {
        return piece_id;
    }

    /**
     * 设置棋子
     *
     * @param piece_id 棋子
     */
    public void setPiece_id(byte piece_id) {
        this.piece_id = piece_id;
    }

    /**
     * 获取移动方向
     *
     * @return MoveDirection 移动方向
     */
    public MoveDirection getDirection() {
        return direction;
    }

    /**
     * 设置移动方向
     *
     * @param direction 移动方向
     */
    public void setDirection(MoveDirection direction) {
        this.direction = direction;
    }

    /**
     * 比较当前动作与指定动作是否相同
     *
     * @param move 被比较的动作
     * @return true  相同<br>
     * 		   false 不相同
     */
    public boolean compareTo(Move move) {
        // TODO 自动生成的方法存根
        if(piece_id == move.piece_id && direction==move.direction) return true;
        else return false;
    }





    /*
     * 用途在于使Move类可以作为Map对象的Key值
     */
    @Override
    public boolean equals(Object object){
        Move move=(Move) object;
        return compareTo(move);
    }

    @Override
    public Move clone(){
        Move move=new Move(this.piece_id,this.direction);
        return move;

    }

    /**
     * 输出信息
     *
     * @param tabNum tab键数量
     */
    // public void printMove(int tabNum) {
    //     // TODO 自动生成的方法存根
    //     for(int i=0;i<tabNum;i++) System.out.print("	");
    //     System.out.println("Move Info：");
    //     for(int i=0;i<tabNum;i++) System.out.print("	");
    //     System.out.println("Piece:"+Piece.toString(piece_id));
    //     for(int i=0;i<tabNum;i++) System.out.print("	");
    //     System.out.println("MoveDirection:"+direction);
    // }

    /*
     * 转化为文本格式
     */
    @Override
    public String toString(){
        return Piece.toString(piece_id).trim()+" "+direction;
    }

    /*
     * 哈希编码，使Move类可以作为Map对象的Key值
     */
    public int hashCode() {
    	return this.piece_id * 10 + this.direction.hashCode();
    }
}
