package ahu.ewn.game;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import ahu.ewn.board.ChessBoard;
import ahu.ewn.board.Piece;
import ahu.ewn.board.Piece_Type;

/**
 * 棋谱，用于记录一局对弈过程，可将对弈过程保存为文本文件，
 * 棋谱格式以2018年《中国大学生计算机博弈大赛棋谱标准说明书》为准
 */
public class GameRecord {

	//参数及构造函数
	/**
	 * 对弈双方的名称执棋信息
	 */
	private Map<Piece_Type, String> players;
	/**
	 * 先手方的棋子颜色
	 */
	private Piece_Type firstPlayer;
	/**
	 * 获胜方的棋子颜色
	 */
	private Piece_Type winner;
	/**
	 * 比赛时间
	 */
	private String date;
	/**
	 * 比赛地点
	 */
	private String place;
	/**
	 * 比赛名称
	 */
	private String competition_Name;
	/**
	 * 初始棋盘布局
	 */
	private ChessBoard initBoard;
	/**
	 * 下棋动作序列
	 */
	private ArrayList<Step> steps;
	
	/**
	 * 一步下棋动作，记录了行棋方、骰子点数、走子动作
	 */
	public class Step{
		/**
		 * 行棋方
		 */
		public Piece_Type player;
		/**
		 * 骰子点数
		 */
		public byte dice;
		/**
		 * 走子动作
		 */
		public Move move;
	}

	/**
	 * 构造函数，创建一个空棋谱
	 */
	public GameRecord() {
		this.players = new ConcurrentHashMap<Piece_Type, String>();
		this.winner = Piece_Type.NULL;
		this.firstPlayer = Piece_Type.NULL;
		this.updateDate();
		this.place = "线上";
		this.competition_Name = "2022CCGC";
		this.initBoard = new ChessBoard();
		this.steps = new ArrayList<Step>();
	}




	/**
	 * 获取棋谱
	 * 
	 * @return ArrayList 走子动作序列
	 */
	public ArrayList<Step> getSteps(){
		return this.steps;
	}
	
	/**
	 * 增加一个下棋动作
	 * 
	 * @param dice 骰子点数
	 * @param move 下棋动作
	 */
	public void push(byte dice, Move move) {
		Step step = new Step();
		step.player = Piece.getType(move.getPiece_id());
		step.dice = dice;
		step.move = move.clone();
		
		if(this.steps.size() == 0) this.firstPlayer = step.player;
		this.steps.add(step);
	}
	
	/**
	 * 移除一个下棋动作，即悔棋
	 * 
	 * @return 悔掉的下棋动作。如果已经悔至初始棋盘状态，返回null
	 */
	public Step pop() {
		if(this.steps.size() == 0) return null;
		Step step = this.steps.remove(this.steps.size() - 1);
		return step;
	}
	
	/**
	 * 获取先手方
	 * 
	 * @return PieceType 先手方
	 */
	public Piece_Type getFirstPlayer() {
		return this.firstPlayer;
	}
	
	/**
	 * 获取指定步数的棋盘状态
	 * 
	 * @param stepNum 下棋步数
	 * @return ChessBoard 第stepNum步下棋后的棋盘
	 */
	public ChessBoard getBoard(int stepNum) {
		ChessBoard board = this.initBoard.clone();
		for(int i = 0; i < stepNum; i++) {
			Step step = this.steps.get(i);
			board.pieceMove(step.move);
		}
		return board;
	}
	
	/**
	 * 获取初始棋盘布局
	 * 
	 * @return ChessBoard 初始棋盘布局
	 */
	public ChessBoard getInitBoard() {
		return initBoard;
	}

	/**
	 * 设置初始棋盘布局
	 * 
	 * @param initBoard 初始棋盘布局
	 */
	public void setInitBoard(ChessBoard initBoard) {
		this.initBoard = initBoard;
	}
	
	/**
	 * 设置对弈玩家
	 * 
	 * @param players 对弈玩家
	 */
	public void setPlayers(Player... players) {
		for(Player player: players) {
			this.players.put(player.getTurn(), player.getLabel());
		}
	}
	
	/**
	 * 获取对弈双方的名称
	 * 
	 * @return Map 对弈双方的名称
	 */
	public Map<Piece_Type, String> getPlayerNames(){
		return this.players;
	}
	
	/**
	 * 设置获胜方
	 * 
	 * @param player 获胜方的棋子颜色
	 */
	public void setWinner(Piece_Type player) {
		this.winner = player;
	}
	
	/**
	 * 获取获胜方
	 * 
	 * @return PieceType 获胜方的棋子颜色
	 */
	public Piece_Type getWinner() {
		return this.winner;
	}
	
	/**
	 * 获取指定玩家的名称
	 * 
	 * @param player 玩家的棋子颜色
	 * @return String 玩家名称
	 */
	public String getPlayerName(Piece_Type player) {
		return this.players.get(player);
	}
	
	/**
	 * 更新当前时间为比赛时间
	 */
	public void updateDate() {
		Date dt = new Date();   
	    //最后的aa表示“上午”或“下午”    HH表示24小时制    如果换成hh表示12小时制   
	    SimpleDateFormat sdf = new SimpleDateFormat("yyyy.MM.dd HH:mm");   
	    this.date = sdf.format(dt);
	}

	/**
	 * 获取比赛时间
	 * 
	 * @return String 比赛时间
	 */
	public String getDate() {
		return date;
	}

	/**
	 * 设置指定的比赛时间
	 * 
	 * @param date 比赛时间
	 */
	public void setDate(String date) {
		this.date = date;
	}

	/**
	 * 获取比赛地点
	 * 
	 * @return String 比赛地点
	 */
	public String getPlace() {
		return place;
	}

	/**
	 * 设置比赛地点
	 * 
	 * @param place 比赛地点
	 */
	public void setPlace(String place) {
		this.place = place;
	}

	/**
	 * 获取比赛名称
	 * 
	 * @return String 获取比赛名称
	 */
	public String getCompetition_Name() {
		return competition_Name;
	}

	/**
	 * 设置比赛名称
	 * 
	 * @param competition_Name 比赛名称
	 */
	public void setCompetition_Name(String competition_Name) {
		this.competition_Name = competition_Name;
	}
	
	/**
	 * 获取当局的下棋步数
	 * 
	 * @return 下棋步数
	 */
	public int size() {
		return this.steps.size();
	}
	
	/**
	 * 按照2018年《中国大学生计算机博弈大赛棋谱标准说明书》标准生成棋谱文件的文件名
	 * 
	 * @return 文件名
	 */
	public String getFileName() {
		Date dt = new Date();
		SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddHHmm");   
	    String time = sdf.format(dt);
	    String firstName = this.players.get(firstPlayer);
	    String lastName = this.players.get(firstPlayer== Piece_Type.BLUE? Piece_Type.RED: Piece_Type.BLUE);
	    String win = "null";
	    if(winner == firstPlayer) {
	    	win = "先手胜";
	    }
	    else if(winner != Piece_Type.NULL) {
	    	win = "后手胜";
	    }
	    return new String("WTN-"+firstName+"vs"+lastName+"-"+win+time);
	}
	
	/*
	 * 按照2018年《中国大学生计算机博弈大赛棋谱标准说明书》标准生成棋谱文件的内容
	 */
	public String toString() {
		StringBuilder str = new StringBuilder();
		
		// 1 添加比赛信息
		str.append("#");
		// 1-1 添加先手名称
		str.append("[");
		if(this.firstPlayer == Piece_Type.NULL) {
			str.append("null");
		}
		else {
			str.append(this.players.get(this.firstPlayer));
		}
		str.append("]");
		// 1-2 添加后手名称
		str.append("[");
		if(this.firstPlayer == Piece_Type.NULL) {
			str.append("null");
		}
		else {
			Piece_Type lastPlayer = this.firstPlayer== Piece_Type.BLUE? Piece_Type.RED: Piece_Type.BLUE;
			str.append(this.players.get(lastPlayer));
		}
		str.append("]");
		// 1-3 添加获胜方
		str.append("[");
		if(this.winner == Piece_Type.NULL) str.append("null");
		else if(this.winner == this.firstPlayer) str.append("先手胜");
		else str.append("后手胜");
		str.append("]");
		// 1-4 添加比赛时间和地点
		str.append("[");
		str.append(this.date + " " + this.place);
		str.append("]");
		// 1-5 添加比赛名称
		str.append("[");
		str.append(this.competition_Name);
		str.append("]");
		
		str.append(";\n");
		
		// 2 添加初始布局
		str.append(this.board2string());
		str.append("\n");
		
		// 3 添加走法序列
		for(int t = 0; t < this.steps.size(); t++) {
			Step step = this.steps.get(t);
			byte dice = step.dice;
			byte piece = step.move.getPiece_id();
			ChessBoard toBoard = this.getBoard(t+1);
			int[] toPoint = toBoard.getLocation(piece);
			
			str.append(String.valueOf(t+1) + ":");
			str.append(String.valueOf(dice) + ";");
			str.append("(");
			if(Piece.getType(piece) == Piece_Type.BLUE){
				str.append("B"+String.valueOf(Piece.getNumber(piece)));
			}
			else if(Piece.getType(piece) == Piece_Type.RED){
				str.append("R"+String.valueOf(Piece.getNumber(piece)));
			}
			str.append(",");
			str.append(this.rowcol2string(toPoint[0], toPoint[1]));
			str.append(")");
			if(t != this.steps.size() - 1) str.append("\n");
		}
		
		return str.toString();
	}
	
	/**
	 * 按照2018年《中国大学生计算机博弈大赛棋谱标准说明书》标准存储棋谱文件
	 * 
	 * @param fileName 文件名（绝对路径）
	 */
	// public void save(String fileName) {
	// 	File file=new File(fileName);
    // 	try{
    // 		FileWriter writer = new FileWriter(file);
    // 		writer.write(this.toString());
    // 		writer.flush();
    // 		writer.close();
    // 	}
    // 	catch(IOException ex){
    // 		new IOException("Error saving data set file!",ex).printStackTrace();
    // 	}
	// }
	
	/**
	 * 按照2018年《中国大学生计算机博弈大赛棋谱标准说明书》标准将ChessBoard转化为String
	 * 
	 * @return String
	 */
	private String board2string() {
		StringBuilder str = new StringBuilder();
		// 1 添加红方棋子位置
		str.append("R:");
		for(byte number=1; number<=6; number++) {
			int[] rowcol = this.initBoard.getLocation(Piece.createprice_id(Piece_Type.RED, number));
			str.append(this.rowcol2string(rowcol[0], rowcol[1]) + "-" + String.valueOf(number));
			if(number != 6) str.append(";");
		}
		str.append("\n");
		// 1 添加蓝方棋子位置
		str.append("B:");
		for(byte number=1; number<=6; number++) {
			int[] rowcol = this.initBoard.getLocation(Piece.createprice_id(Piece_Type.BLUE, number));
			str.append(this.rowcol2string(rowcol[0], rowcol[1]) + "-" + String.valueOf(number));
			if(number != 6) str.append(";");
		}

		return str.toString();
	}
	
	/**
	 * 按照2018年《中国大学生计算机博弈大赛棋谱标准说明书》标准将行列转化为String
	 * 
	 * @param row 行号
	 * @param col 列号
	 * @return String
	 */
	private String rowcol2string(int row, int col) {
		String[] colStr = new String[]{"A", "B", "C", "D", "E"};
		String[] rowStr = new String[]{"5", "4", "3", "2", "1"};
		return new String(colStr[col] + rowStr[row]);
	}

	/**
	 * 设置先行方
	 * 
	 * @param firstTurn 先行方颜色
	 */
	public void setFirstPlayer(Piece_Type firstTurn) {
		// TODO 自动生成的方法存根
		this.firstPlayer = firstTurn;
	}
}
