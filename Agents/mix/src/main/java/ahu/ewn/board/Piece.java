package ahu.ewn.board;

/**
 * 棋子。每个棋子有不同的的编码id，{0，11~16，21~26｝
 * 0表示无棋子；
 * 11~16表示蓝方的1~6号棋子；
 * 21~26表示红方的1~6号棋子。
 */
public class Piece{

	/**
	 * 创建一个棋子,根据棋子类型和编号返回编码id
	 *
	 * @param type 棋子类型
	 * @param number 棋子编号
	 * @return 棋子ID
	 */
	public static byte createprice_id(Piece_Type type, byte number) {
		byte id = 0;
		if (type == Piece_Type.RED)
			id = (byte) (20 + number);
		else if (type == Piece_Type.BLUE)
			id = (byte) (10 + number);
		else id=0;
		return id;
	}

	/**
	 * 获取棋子类型
	 *
	 * @param id 棋子ID
	 * @return PieceType 棋子类型
	 */
	public static final Piece_Type getType(byte id){
		if (id / 10 == 2)
			return Piece_Type.RED;
		else if (id / 10 == 1)
			return Piece_Type.BLUE;
		else
			return Piece_Type.NULL;
	}

	/**
	 * 获取棋子号码
	 *
	 * @param id 棋子id
	 * @return 编号
	 */
	public static final byte getNumber(byte id) {
		return (byte) (id % 10);
	}

	/**
	 * 获取ID号
	 *
	 * @param type 棋子类型
	 * @param number 棋子编号
	 * @return id
	 */
	public static final byte getID(Piece_Type type, byte number) {

		return createprice_id(type,number);
	}

	/**
	 * 将棋子转换成文本输出
	 * 例：
	 * System.out.println(12) 输出结果：  B2
	 * System.out.println(22) 输出结果：  R2
	 * 
	 * @param piece_id 棋子
	 * @return String
	 */
	public static String toString(byte piece_id){
		if(Piece.getType(piece_id) == Piece_Type.BLUE){
			return new String("B"+String.valueOf(Piece.getNumber(piece_id))+"\t");
		}
		else if(Piece.getType(piece_id) == Piece_Type.RED){
			return new String("R"+String.valueOf(Piece.getNumber(piece_id))+"\t");
		}
		else return new String("-" + "\t");
	}
}