package ahu.ewn.strategy.move.metekaluo;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import ahu.ewn.board.ChessBoard;
import ahu.ewn.board.Piece_Type;
import ahu.ewn.game.Game;
import ahu.ewn.game.Move;
import ahu.ewn.game.MoveSearch;
import ahu.ewn.game.Player;
import ahu.ewn.strategy.evaluation.EvaluationFunction;
import ahu.ewn.strategy.evaluation.FenxiPinggu;
import ahu.ewn.game.initial.StaticInit;
import ahu.ewn.strategy.move.MoveStrategy;
import ahu.ewn.strategy.move.pinggu.StaticEvaluationMove;
import java.util.concurrent.*;


/**
 * 随机产生下棋动作
 *
 */
public class Mengtekaluo extends MoveStrategy {

	private Map<Integer, Move> moveMap =  new ConcurrentHashMap<>();
	

    /**
     * 构造函数
     */
    public Mengtekaluo(){
        super();
        setLabel("RandomMove");
    }

    @Override
    public Move getMove(Game game, byte dice) {
    	/**
		 * 采用蒙特卡洛搜索算法实现的代码。
		 */
		
		
		//获取当前的棋盘
		ChessBoard board = game.getNowBoard();
		//获取当前的玩家颜色
		Piece_Type player = game.getNowPlayer().getTurn();
		//获取所有可行步法
		
		Map<Move, ChessBoard> legalMoves = MoveSearch.getLegalMovesByDice(board, player, dice);
		List<Move> keyList = new ArrayList<Move>(legalMoves.keySet());
		//定义最好步法以及大数据获胜轮数
		Move bestMove = null;
		//ExecutorService executorService = Executors.newFixedThreadPool(keyList.size());

		
		//int maxwin = -1;

	    //board.show();
		//检验代码
		// for(int i = 0; i < keyList.size(); i++){
		// 	System.out.print(keyList.get(i).getPiece_id()+" ");
		// 	System.out.print(keyList.get(i).getDirection()+" ");
		// }
		// System.out.println(" ");
		//List<Runnable> runnables = new ArrayList<Runnable>();
		for (int i = 0;i<keyList.size();i++){
			ChessBoard boardStep = legalMoves.get(keyList.get(i));
			int j = i;
    		// Runnable task = () -> {
        		int winNum = MonCa(boardStep, player, game.getProbe());
				moveMap.put(winNum, keyList.get(j));
        	// 这里可以进行其他操作
    		// };
			//runnables.add(task);
			// int winNum = MonCa(boardStep, player);
			// if(winNum > maxwin){
			// 	maxwin = winNum;
			// 	bestMove = keyList.get(i);
			// }
		}
		
		// for(int i = 0; i < runnables.size(); i++){
		// 	executorService.execute(runnables.get(i));
		// }
		
		// executorService.shutdown();

		// try {
        //     // 等待所有线程执行完成（超时时间设为1小时）
        //     if (!executorService.awaitTermination(1, TimeUnit.HOURS)) {
        //         System.out.println("等待超时，部分任务可能未完成。");
        //     }
        // } catch (InterruptedException e) {
        //     e.printStackTrace();
        // }

		int max = -1;

		for (int key : moveMap.keySet()) {
            if (key > max) {
                max = key;
            }
        }

		bestMove = moveMap.get(max);
		moveMap.clear();
		
		return bestMove;
			
    }
	//计算一种情况winNum的一次线程
	

    private int MonCa(ChessBoard board, Piece_Type player, int probe) {
    	  // 对弈轮数
			int game = probe;
			int pieceWinNum = 0;

			// 先手方，即对方先下棋
			Piece_Type firstPlayer = Piece_Type.getOppoType(player);
			EvaluationFunction customEvaluate = new FenxiPinggu();
			// 设置红蓝双方棋手，我方棋手
			Player play1 = new Player(player, new StaticInit(),new StaticEvaluationMove(customEvaluate));
			// 指定红方的布局策略和下棋策略
			Player play2 = new Player(Piece_Type.getOppoType(player), new StaticInit(), new StaticEvaluationMove(customEvaluate));
			// 初始化红蓝双方
			Player bluePlayer = null;
			Player redPlayer  = null;
			// 判断红蓝双方
			if (player == Piece_Type.BLUE) {
				bluePlayer = play1;
				redPlayer  = play2;
			}else{
				bluePlayer = play2;
				redPlayer  = play1;
			}
			
			// 定义一局游戏，并设置玩家为上面定义的玩家
			Game game1 = new Game();
			
			game1.setPlayer(bluePlayer);
			game1.setPlayer(redPlayer);

			// 对弈轮数的迭代
			for(int cnt = 1; cnt <= game; cnt++) {
				// 存储之前的棋盘
				ChessBoard board1 = board.clone();
				// 重置游戏，生成初始布局
				game1.reset(firstPlayer, board1);
				// 红蓝双方轮流行棋，直至游戏结束
				while(game1.isEnd()==false) {
					// 随机生成一个骰子点数
					byte dice = game1.getDice();
					// 行棋方的走子策略产生一个合法走法
					Move move = game1.getNowPlayer().getMoveStrategy().getMove(game1, dice);
					// 执行合法走法，即下一步棋
					game1.step(dice, move);
				}
				// 统计获胜方
				if (player == Piece_Type.BLUE) {
					if(game1.getWinner()== Piece_Type.BLUE) {
						pieceWinNum += 1;
					}
				}else {
					if(game1.getWinner()== Piece_Type.RED) {
						pieceWinNum += 1;
					}
				}
			}
			return pieceWinNum;
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

 
    public void processEnd() {
        // TODO 自动生成的方法存根

    }

}
