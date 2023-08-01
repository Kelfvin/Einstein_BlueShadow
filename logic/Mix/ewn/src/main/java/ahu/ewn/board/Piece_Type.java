package ahu.ewn.board;

/**
 * 棋盘上的’棋子‘类型,BLUE蓝方；RED红方；NULL无棋子
 */
public enum Piece_Type {
	/**
	 * 蓝色
	 */
	BLUE,
	/**
	 * 红色
	 */
	RED,
	/**
	 * 无棋子
	 */
	NULL;

	public static Piece_Type getOppoType(Piece_Type type){
		if(type == Piece_Type.RED) return Piece_Type.BLUE;
		else if(type == Piece_Type.BLUE) return Piece_Type.RED;
		else return Piece_Type.NULL;
	}
}