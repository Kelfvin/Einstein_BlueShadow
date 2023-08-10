package ahu.ewn.strategy.move;

import ahu.ewn.board.Piece_Type;
import ahu.ewn.game.Game;
import ahu.ewn.game.Move;

/**
 * 走子策略基类，getMove方法为核心方法，用于生成走子动作
 */
abstract public class MoveStrategy{

    /**
     * 标签
     */
    private String label;

    /**
     * 该策略预测的价值，用于界面显示
     */
    protected double value;
    
    /**
     * 搜索深度，用于界面显示
     */
    protected int maxDepth;
	/**
	 * 迭代次数，用于界面显示，一般用不到
	 */
	protected int visitNum;
	/**
	 * 策略执行时间，用于界面显示
	 */
	protected long runTime;

    /**
     * 获取标签
     *
     * @return 标签
     */
    public String getLabel(){
        return this.label;
    }

    /**
     * 设置标签
     *
     * @param label 标签
     */
    public void setLabel(String label){
        this.label=label;
    }

    @Override
    public String toString(){
        return label;
    }

    /**
     * 获得当前游戏状态下的一步走子动作
     *
     * @param game
     *            当前游戏状态，包含了对弈的全部信息
     * @param dice
     *            骰子数
     * @return Move 走子动作
     */
    abstract public Move getMove(Game game, byte dice);

    /**
     * 处理敌方下棋动作
     *
     * @param move 敌方的下棋动作
     */
    abstract public void processEnemyMove(Move move);

    /**
     * 初始化，仅游戏开始时调用
     *
     * @param game 游戏状态
     * @param myTurn 我方棋子颜色
     */
    abstract public void processStart(Game game, Piece_Type myTurn);

    /**
     * 处理悔棋动作
     *
     * @param game 悔棋后的游戏状态
     * @param move 悔的动作
     */
    abstract public void processBack(Game game, Move move);

    /**
     * 游戏结束时调用
     */
    abstract public void processEnd();

    /**
     * 获取策略预测的价值
     *
     * @return double 价值
     */
    public double getMoveValue(){
        return this.value;
    }
    
    /**
     * 获取搜索深度
     * 
     * @return int 搜索深度
     */
    public int getMaxDepth() {
		return this.maxDepth;
	}
	
	/**
	 * 获取迭代次数
	 * 
	 * @return 迭代次数
	 */
	public int getVisitNum() {
		return this.visitNum;
	}
	
	/**
	 * 获取运行时间
	 * 
	 * @return 运行时间
	 */
	public long getRunTime() {
		return this.runTime;
	}

    /**
     * 偷懒写法
     * @see java.lang.Object#clone()
     */
    @Override
    public MoveStrategy clone(){
        return this.clone();
    }
}
