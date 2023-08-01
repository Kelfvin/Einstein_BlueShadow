package ahu.ewn.strategy.evaluation;



import ahu.ewn.board.ChessBoard;
import ahu.ewn.board.Piece_Type;

/**
 * 随机估值，返回随机数
 * 
 *
 */
public class RandomPinggu extends EvaluationFunction {
	
	/**
	 * 构造函数，创建一个随机估值函数
	 */
	public RandomPinggu() {
		setLabel("RandomEvaluate");
	}

	@Override
	public double getValue(ChessBoard board, Piece_Type type,int which) {
		// TODO 自动生成的方法存根
		return new java.util.Random().nextDouble()*2 - 1;
	}

}
