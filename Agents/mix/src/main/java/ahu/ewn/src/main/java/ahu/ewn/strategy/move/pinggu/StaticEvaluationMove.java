package ahu.ewn.strategy.move.pinggu;

import ahu.ewn.board.ChessBoard;
import ahu.ewn.board.Piece_Type;
import ahu.ewn.game.Game;
import ahu.ewn.game.Move;
import ahu.ewn.game.MoveSearch;
import ahu.ewn.strategy.evaluation.EvaluationFunction;
import ahu.ewn.strategy.move.MoveStrategy;

import java.util.Map;

/**
 * 根据指定的估值函数选择估值最高的走法，即界面中的“直接估值”策略<br>
 * 例如：<br>
 * 假设目前的合法走法有三个：[蓝3左  蓝3前  蓝3右]<br>
 * 这三个走法行棋后产生三个对应的棋盘：[board1 board2 board3]<br>
 * 经evaluateFunction计算，这三个棋盘对蓝方的价值分别为[0.2 0.6 0.1]<br>
 * 则该策略会认为 蓝3前 是最佳走法
 *
 * 
 *
 */
public class StaticEvaluationMove extends MoveStrategy {

    /**
     * 估值函数
     */
    private EvaluationFunction evaluateFunction;

    /**
     * 构造函数，指定估值函数
     *
     * @param function 估值函数
     */
    public StaticEvaluationMove(EvaluationFunction function){
        super();
        this.evaluateFunction=function;
        setLabel("StaticEvaluationMove");
    }

    /**
     * 获取估值函数
     *
     * @return EvaluateFunction 估值函数
     */
    public EvaluationFunction getEvaluateFunction(){
        return this.evaluateFunction;
    }

    /**
     * 设置估值函数
     *
     * @param evaluateFunction 估值函数
     */
    public void setEvaluationFunciton(EvaluationFunction evaluateFunction){
        this.evaluateFunction=evaluateFunction;
    }

    @Override
    public Move getMove(Game game, byte dice) {
        // TODO 自动生成的方法存根

        Piece_Type turn= game.getNowPlayer().getTurn();
        ChessBoard board= game.getNowBoard();

        Map<Move,ChessBoard> moves= MoveSearch.getLegalMovesByDice(board, turn, dice);
        double maxValue=Integer.MIN_VALUE;
        Move bestMove=null;
        for(Map.Entry<Move, ChessBoard> entry:moves.entrySet()){
            double tem = evaluateFunction.getValue(entry.getValue(), turn,1);
            if(tem >= maxValue){
                maxValue=tem;
                bestMove=entry.getKey();
            }
        }
        //System.out.println(" ");
        this.value=maxValue;

        if(bestMove==null){
//		bestMove=moves.keySet().iterator().next();
        }

        return bestMove;
    }

    @Override
    public void processEnemyMove(Move move) {
        // TODO 自动生成的方法存根

    }

    @Override
    public void processStart(Game game, Piece_Type myTurn) {
        // TODO 自动生成的方法存根

    }

    @Override
    public void processBack(Game game, Move move) {
        // TODO 自动生成的方法存根

    }

    @Override
    public void processEnd() {
        // TODO 自动生成的方法存根

    }

}
