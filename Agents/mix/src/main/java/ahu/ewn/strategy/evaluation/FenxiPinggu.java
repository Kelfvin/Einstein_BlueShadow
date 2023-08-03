package ahu.ewn.strategy.evaluation;

import java.util.List;

import ahu.ewn.board.ChessBoard;
import ahu.ewn.board.Piece;
import ahu.ewn.board.Piece_Type;

/**
 * 自定义估值函数，需要在此类中完善估值的代码。界面中的“直接估值”策略里的“超级估值”就是指这个类
 *
 */
public class FenxiPinggu extends EvaluationFunction{

	//		int distancered[][] = { { 0, 1, 2, 3, 4 }, { 1, 1, 2, 3, 4 }, { 2, 2, 2, 3, 4 }, { 3, 3, 3, 3, 4 }, { 4, 4, 4, 4, 4 } };
//		int distanceblue[][] = { { 4, 4, 4, 4, 4 }, { 4, 3, 3, 3, 3 }, { 4, 3, 2, 2, 2 }, { 4, 3, 2, 1, 1 }, { 4, 3, 2, 1, 0 } };
	//概率数组
	//6个棋子的能动点数
	int p[] = new int[6];
	int p2[] = new int[6];

	//六个棋子的获胜步数差，用于计算我方价值R
	int distance[]=new int [6];
	int distance2[]=new int [6];
	//我方获胜价值+
	double R=0;

	//定义棋盘上双方棋子的位置价值用于计算进攻值
	double boardvred[][] = { { 0, 1, 1, 1, 1 }, { 1, 2, 2, 2, 2.5 }, { 1, 2, 4, 4, 5 }, { 1, 2, 4, 8, 10 }, { 1, 2.5, 5, 10, 16 } };
	double boardvblue[][] = { { 16, 10, 5, 2.5, 1 }, { 10, 8, 4, 2, 1 }, { 5, 4, 4, 2, 1 }, { 2.5, 2, 2, 2, 1 }, { 1, 1, 1, 1, 0 } };
	double value[] = new double [6];
	double value2[] = new double [6];
	double attack = 0.0;
	double attack2 = 0.0 ;

	//定义棋子 三个方向上的的棋子的价值（计算威胁数组）
	double a=0,b=0,c=0;
	//定义威胁值数组，用于计算威胁值threat
	double maxvalue[] = new double[6];
	double threat = 0.0;

	//定义最终的进攻值+，被狙击值-，被威胁值-
	double exp1=0.0,exp2=0.0,theat1 = 0.0;


	@Override
	public double getValue(ChessBoard board, Piece_Type type, int which) {
		// TODO 自动生成的方法存根
		dateclear();
		getvalue_type(board,type);

//		System.out.println("估值为:"+getvalue_return(which));
//		showinformation();

		return getvalue_return(which);
	}

	void getvalue_type(ChessBoard board, Piece_Type type){
		//board.show();

		double[][] boardmvalue = getboardvalue(type);
		double[][] boardyvalue = getboardvalue(Piece_Type.getOppoType(type));
		//获取我方的所有棋子
		List<Byte> pieces = board.getPieces(type);

		//遍历
		for (int i =0; i<pieces.size();i++){
			double infvalue;
			//根据指定的棋子，求能使该棋子移动的骰子点数；是p[i]
			List<Byte> count = board.getDicesByPiece(pieces.get(i));
			p[i] = count.size();
			//获得棋子的位置
			int[] rowcol = board.getLocation(pieces.get(i));
			//求出该棋子在棋盘上的价值
			distance[i] = getdistance(rowcol,type);
			if(distance[i]==0) infvalue =9999;
			if(distance[i]==1) {
				infvalue = 5/2*Math.pow(2,4-distance[i]);
			} else if(rowcol[1]==0||rowcol[1]==4||rowcol[0]==0||rowcol[0]==4) {
				infvalue = 5*Math.pow(2,2-distance[i]);
			} else{
				infvalue=(4-distance[i])*Math.pow(2,4-distance[i])/2;
			}
			R+=p[i]*infvalue/6;
			//获胜期望值
			value[i] = boardmvalue[rowcol[0]][rowcol[1]]*3;
			//求威胁值
			int tem = 0;
			if(type==Piece_Type.RED && rowcol[0] <4 && rowcol[1] <4 ) { tem = 1; }
			if(type==Piece_Type.BLUE && rowcol[0] >0 && rowcol[1] >0 ){ tem = -1; }
			if(tem!=0) {
				if (Piece.getType(board.getBoard()[rowcol[0] + tem][rowcol[1]]) == Piece_Type.getOppoType(type)) {
					a = boardyvalue[rowcol[0] + tem][rowcol[1]];
				}
				if (Piece.getType(board.getBoard()[rowcol[0]][rowcol[1] + tem]) == Piece_Type.getOppoType(type)) {
					b = boardyvalue[rowcol[0]][rowcol[1] + tem];
				}
				if (Piece.getType(board.getBoard()[rowcol[0] + tem][rowcol[1] + tem]) == Piece_Type.getOppoType(type)) {
					c = boardyvalue[rowcol[0] + tem][rowcol[1] + tem];
				}
			}
			double max = (a > b) ? a : b;
			max = (max > c) ? max : c;
			maxvalue[i] = max;
			a=0;b=0;c=0;
		}
		//我方的进攻值期望和威胁值期望
		for (int i =0; i<pieces.size();i++){
			attack = attack + p[i]*value[i];
			threat = threat + maxvalue[i]*p[i];
			//System.out.println(maxvalue[i]+" "+p[i]);
		}

		//获取对方的棋子
		List<Byte> pieces2 = board.getPieces(Piece_Type.getOppoType(type));
		//遍历
		for (int i =0; i<pieces2.size();i++){
			//根据指定的棋子，求能使该棋子移动的骰子点数；是p2[i]
			List<Byte> count2 = board.getDicesByPiece(pieces2.get(i));
			p2[i] = count2.size();
			//获得棋子的位置
			int[] rowcol2 = board.getLocation(pieces2.get(i));
			//求出该棋子在棋盘上的价值
			value2[i] = boardyvalue[rowcol2[0]][rowcol2[1]];
		}
		//对方的进攻值期望
		for (int i =0; i<pieces2.size();i++){
			attack2 = attack2 + p2[i]*value2[i];
		}
	}

	double getvalue_return(int which){
		exp1 = attack;
		exp2 = -attack2;
		theat1 = -threat;

		if(which == 0){
			return 10*exp1 + 5*exp2 + 1*theat1;
		}

		else if(which == 1){
			int aa=0;
			int ab=0;
			for(int i=0;i<6;i++) {
				if(distance[i]>aa) aa=distance[i];
			}
			for(int i=0;i<6;i++) {
				if(distance2[i]>ab) ab= distance2[i];
			}
			if(aa>=2) {
				if(aa<ab) //我方优势，主要考虑进攻值不急取胜
					return 5*exp1 + 5*exp2 + 1*theat1 + 1*(R) + 10*exp1;
				else //我方劣势，主要考虑获胜值与被阻击值
					return 5*exp1 + 5*exp2 + 1*theat1 + 2*(R) + 5*exp2;
			}
			else //直接获胜好吧
				return 3*(R) + 5*exp1 + 5*exp2 + 1*theat1;
		}

		//System.out.println("估值方法错误");
		return 0.0;
	}

	double[][] getboardvalue(Piece_Type type){
		if(type == Piece_Type.BLUE) return boardvblue;
		else if(type == Piece_Type.RED) return boardvred;
		else return null;
	}

	int getdistance(int[] rowcol, Piece_Type type){
		if(type == Piece_Type.BLUE) {
			if (rowcol[0] >= rowcol[1]) {
				return rowcol[0];
			} else {
				return rowcol[1];
			}
		}else if(type == Piece_Type.RED){
			if(rowcol[0]>=rowcol[1]) {
				return 4-rowcol[1];
			} else {
				return 4-rowcol[0];
			}
		}
		return 0;
	}

	// void showinformation(){
	// 	System.out.println("["+R+"][" + exp1+" "+exp2+"][" + theat1 + "]");
	// }

	void dateclear(){
		p = new int[6];
		p2  = new int[6];
		distance = new int [6];
		distance2 =new int [6];
		R=0;
		attack2 = 0.0;
		attack = 0.0; threat = 0.0;
		exp1=0.0;exp2=0.0;theat1 = 0.0;
		value = new double [6];
		value2 = new double [6];
		a=0;b=0;c=0;
		maxvalue = new double[6];
	}
}
