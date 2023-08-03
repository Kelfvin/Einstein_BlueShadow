package ahu.ewn.game;

import ahu.ewn.board.Piece_Type;
import ahu.ewn.game.initial.InitStrategy;
import ahu.ewn.game.initial.StaticInit;
import ahu.ewn.strategy.move.MoveStrategy;

/**
 * 玩家类。存储玩家的对弈信息和策略，包括所持棋子的颜色、布局策略、下棋策略，以及预设运行时间
 */
public class Player{

    /**
     * 执棋的颜色
     */
    private Piece_Type turn;

    /**
     * 初始布局策略
     */
    private InitStrategy initStrategy;

    /**
     * 下棋策略
     */
    private MoveStrategy moveStrategy;

    /**
     * 对弈的限定时间(国赛要求为每盘每方4分钟，暂时没用到该属性)
     */
    private long presettingTime;

    /**
     * 运行时间(当前对局中从开始到本次下棋动作结束的时间)
     */
    private long runningTime;

    /**
     * 标签：玩家名称
     */
    private String label;

    /**
     * 构造函数
     * 默认的布局策略和走子策略为随机策略
     *
     * @param turn 所持棋子颜色
     */
    public Player(Piece_Type turn){
        this.turn=turn;
        this.initStrategy = new StaticInit();
       // this.moveStrategy = new RandomMove();
        setLabel(turn.toString());
    }

    /**
     * 构造函数
     *
     * @param turn 所持棋子颜色
     * @param initStrategy 布局策略
     * @param moveStrategy 下棋策略
     */
    public Player(Piece_Type turn, InitStrategy initStrategy, MoveStrategy moveStrategy){
        this.turn=turn;
        this.initStrategy=initStrategy;
        this.moveStrategy=moveStrategy;
        setLabel(turn.toString());
    }

    /**
     * 构造函数
     *
     * @param turn 所持棋子颜色
     * @param initStrategy 初始策略
     * @param moveStrategy 下棋策略
     * @param presettingTime 对弈的限定时间
     */
    public Player(Piece_Type turn, InitStrategy initStrategy, MoveStrategy moveStrategy, long presettingTime){
        this.turn=turn;
        this.initStrategy=initStrategy;
        this.moveStrategy=moveStrategy;
        this.presettingTime=presettingTime;
        setLabel(turn.toString());
    }




    /**
     * 获取所持棋子颜色
     *
     * @return PieceType 所持棋子颜色
     */
    public Piece_Type getTurn() {
        return turn;
    }

    /**
     * 设置所持棋子颜色
     *
     * @param turn 所持棋子颜色
     */
    public void setTurn(Piece_Type turn) {
        this.turn = turn;
    }

    /**
     * 获取初始布局策略
     *
     * @return InitialBoardStrategy 布局策略
     */
    public InitStrategy getInitStrategy() {
        return initStrategy;
    }

    /**
     * 设置初始布局策略
     *
     * @param initStrategy 布局策略
     */
    public void setInitStrategy(InitStrategy initStrategy) {
        this.initStrategy = initStrategy;
    }

    /**
     * 获取下棋策略
     *
     * @return MoveStrategy
     */
    public MoveStrategy getMoveStrategy() {
        return moveStrategy;
    }

    /**
     * 设置下棋策略
     *
     * @param moveStrategy 下棋策略
     */
    public void setMoveStrategy(MoveStrategy moveStrategy) {
        this.moveStrategy = moveStrategy;
    }

    /**
     * 获取限定时间
     *
     * @return long 限定时间
     */
    public long getPresettingTime() {
        return presettingTime;
    }

    /**
     * 设置限定时间
     *
     * @param presettingTime 限定时间
     */
    public void setPresettingTime(long presettingTime) {
        this.presettingTime = presettingTime;
    }

    /**
     * 获取运行时间
     *
     * @return long 运行时间
     */
    public long getRunningTime() {
        return runningTime;
    }

    /**
     * 设置运行时间
     *
     * @param runningTime 运行时间
     */
    public void setRunningTime(long runningTime) {
        this.runningTime = runningTime;
    }

    /**
     * 增加运行时间
     *
     * @param runningTime 运行时间
     */
    public void addRunningTime(long runningTime){
        this.runningTime+=runningTime;
    }

     /**
     * 获取标签
     *
     * @return String 标签
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
        return this.label;
    }
}

