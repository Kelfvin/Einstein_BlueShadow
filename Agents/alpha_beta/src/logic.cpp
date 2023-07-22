#include "logic.h"
#include <qmath.h>
#include <QDebug>
#include <iostream>
#pragma push_macro("slots")
#undef slots


#include <boost/python.hpp>

#pragma pop_macro("slots")



Logic::Logic()
{
    whoplay=0;
    redValueChart={
        {0,2,2,2,2},
        {2,4,4,4,5},
        {2,4,8,8,10},
        {2,4,8,16,20},
        {2,5,10,20,32}
    };
    blueValueChart={
        {32,20,10,5,2},
        {20,16,8,4,2},
        {10,8,8,4,2},
        {5,4,4,4,2},
        {2,2,2,2,1},
    };

    redValue.resize(SIZE);
    blueValue.resize(SIZE);
    redProbability.resize(SIZE);
    blueProbability.resize(SIZE);
    redthreaten.resize(SIZE);
    bluethreaten.resize(SIZE);

    blueprobabilityflag.resize(SIZE);
    for (int i=0;i<SIZE;i++) {
        blueprobabilityflag[i].resize(2);
    }

    redprobabilityflag.resize(SIZE);
    for (int i=0;i<SIZE;i++) {
        redprobabilityflag[i].resize(2);
    }

    virtueTable.resize(LINE);
    for (int i=0;i<LINE;i++) {
        virtueTable[i].resize(LINE);
    }

}


bool Logic::isThereBlue()
{
    for (int i=0;i<LINE;i++) {
        for (int j=0;j<LINE;j++) {
            if(virtueTable[i][j]>0){
                return true;
            }
        }
    }
    return false;
}


bool Logic::isThereRed()
{
    for (int i=0;i<LINE;i++) {
        for (int j=0;j<LINE;j++) {
            if(virtueTable[i][j]<0){
                return true;
            }
        }
    }
    return false;
}

int Logic::judgeResult()
{
    if (virtueTable[0][0] > 0 || !isThereRed())
    {
        //ui->back->setEnabled(true);
        return 1;
    }
    if (virtueTable[4][4] < 0 || !isThereBlue())
    { //ui->back->setEnabled(true);
        return 2;
    }
    return 0;
}

QPoint Logic::blueWhereToGo(int x, int y, int depth, float alpha, float beta)
{

    int a1 = 0; //a用于保存三个方向的棋值
    float val = 0;
    float temp = 0;
    int flag = 0;
    int bestmoveX;
    int bestmoveY;

    if (x > 0 && y > 0 ){ //有左上方
        if (specialDeal(x,y)) {
            return QPoint(x,y);
        }
        a1 = virtueTable[x - 1][y - 1];
        virtueTable[x - 1][y - 1] = virtueTable[x][y];
        virtueTable[x][y] = 0;
       //计算左上点价值

        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] < 0)
                {
                    redReady();

                    val += redProbability[-virtueTable[i][j] - 1] * redMax(i, j, depth, alpha, beta);
                    flag++;
                }


        //最优棋步，杀得对方一个也没有了
        bestmoveX = x - 1;
        bestmoveY = y - 1;
        if (flag == 0)
        {
            bestmoveX = x - 1;
            bestmoveY = y - 1;
            x = bestmoveX;
            y = bestmoveY;
            return QPoint(x,y);
        }
        flag = 0;
        //恢复棋盘
        virtueTable[x][y] = virtueTable[x - 1][y - 1];
        virtueTable[x - 1][y - 1] = a1;
         //蓝棋走左上--------------------------------------------------------


        //蓝棋走左边
        a1 = virtueTable[x - 1][y];
        virtueTable[x - 1][y] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //计算左边价值
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] < 0)
                {
                    redReady();

                    temp += redProbability[-virtueTable[i][j] - 1] * redMax(i, j, depth, alpha, beta);
                    flag++;
                }


        //最优棋步
        if (flag == 0)
        {
            bestmoveX = x - 1;
            bestmoveY = y;
            x = bestmoveX;
            y = bestmoveY;
            return QPoint(x,y);
        }
        flag = 0;
        if (temp < val)
        {
            val = temp;
            bestmoveX = x - 1;
            bestmoveY = y;
        }
        temp = 0;
        //恢复棋盘
        virtueTable[x][y] = virtueTable[x - 1][y];
        virtueTable[x - 1][y] = a1;
       //蓝棋走左边--------------------------------------------------------


       //蓝棋走上方--------------------------------------------------------
        a1 = virtueTable[x][y - 1];
        virtueTable[x][y -1] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //计算上方价值
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] < 0)
                {
                    redReady();

                    temp += redProbability[-virtueTable[i][j] - 1] * redMax(i, j, depth, alpha, beta);
                    flag++;
                }


        if (flag == 0)
        {
            bestmoveX = x;
            bestmoveY = y - 1;
            x = bestmoveX;
            y = bestmoveY;
            return QPoint(x,y);
        }
        flag = 0;
        //最优棋步
        if (temp < val)
        {
            val = temp;
            bestmoveX = x;
            bestmoveY = y - 1;
        }
        //蓝棋走上方--------------------------------------------------------

       //恢复棋盘
        virtueTable[x][y] = virtueTable[x][y - 1];
        virtueTable[x][y - 1] = a1;
        //最终最优棋步
        //qDebug()<<num1;
        /********进行移动*********/
        x = bestmoveX;
        y = bestmoveY;
        return QPoint(x,y);
      /********进行移动*********/
    }
    else if (x == 0) //左边为墙，用不着估值，因为只能走啊
    {
        //qDebug()<<"BlueWhereToGo "<<depth<<":1";
        y = y - 1;
        return QPoint(x,y);
    }
    else if (y == 0) //上方为墙，用不着估值，因为只能走啊
    {
        //qDebug()<<"BlueWhereToGo "<<depth<<":1";
        x = x - 1;
        return QPoint(x,y);
    }


}



bool Logic::specialDeal(int& x,int& y)
{
   //0731 副对角线取消掉
    int num1 = 0;
    int bestmoveX;
    int bestmoveY;
    if (x > 0 && y > 0 && x < 4 && y < 4) //有左上方
    {

        int n = LINE, j = 0, m = 0;
        while (n--)
        {
            for (j = m; j < 5; j++)
            {
                if (virtueTable[j][n] < 0)
                    num1++;
            }
            m++;
        }

        if (whoplay >= 18)
        {

            int chess_number = 0;
            for (int i = 0; i < 5; i++)
                for (int j = 0; j < 5; j++)
                {
                    if (virtueTable[i][j] != 0)
                        chess_number++;
                }
            if (chess_number == 2)
            {
                int x1 = (x - 1);
                int y1 = (y - 1);
                if (virtueTable[x1 - 1][y1 - 1] < 0)
                {

                    /*
                    bestmoveX=x-1;
                    bestmoveY=y;
                    x=bestmoveX;
                    y=bestmoveY;*/
                    if (x == 4)
                    {
                        bestmoveX = x - 1;
                        bestmoveY = y;
                        x = bestmoveX;
                        y = bestmoveY;
                        return true;
                    }
                    if (y == 4)
                    {
                        bestmoveX = x;
                        bestmoveY = y - 1;
                        x = bestmoveX;
                        y = bestmoveY;
                        return true;
                    }
                    else
                    {
                        bestmoveX = x;
                        bestmoveY = y - 1;
                        x = bestmoveX;
                        y = bestmoveY;
                        return true;
                    }
                }
            }
        }

        //0801定式处理
        if (whoplay >= 10)
        {
            int x1 = (x - 1);
            int y1 = (y - 1);
            if (x == 2 && y == 1)
            {
                if (virtueTable[0][0] == 0 && virtueTable[1][0] < 0 && virtueTable[1][1] == 0 && virtueTable[0][1] == 0)
                {
                    bestmoveX = x - 1;
                    bestmoveY = y - 1;
                    x = bestmoveX;
                    y = bestmoveY;
                    return true;
                }
            }
            if (x == 2 && y == 3)
            {
                if (virtueTable[x - 1][y - 1] < 0)
                {

                    if (virtueTable[x1 - 1][y1 - 1] == 0 && virtueTable[x1][y1 - 1] == 0 && virtueTable[x1 - 1][y1] == 0)
                    {
                        bestmoveX = x - 1;
                        bestmoveY = y - 1;
                        x = bestmoveX;
                        y = bestmoveY;
                        return true;
                    }
                }
            }
            if (x == 1 && y == 3)
            {
                if (virtueTable[x - 1][y - 1] < 0)
                {
                    int x1 = (x - 1);
                    int y1 = (y - 1);
                    if (virtueTable[x1][y1 - 1] == 0)
                    {
                        bestmoveX = x - 1;
                        bestmoveY = y - 1;
                        x = bestmoveX;
                        y = bestmoveY;
                        return true;
                    }
                }
            }
            if (x == 1 && y == 2)
            {
                if (virtueTable[x - 1][y - 1] < 0)
                {
                    int x1 = (x - 1);
                    int y1 = (y - 1);
                    if (virtueTable[x1][y1 - 1] == 0)
                    {
                        bestmoveX = x - 1;
                        bestmoveY = y - 1;
                        x = bestmoveX;
                        y = bestmoveY;
                        return true;
                    }
                }
            }

            //0801定式处理
            if (x == 3 && y == 2)
            {
                if (virtueTable[x - 1][y - 1] < 0)
                {

                    if (virtueTable[x1 - 1][y1 - 1] == 0 && virtueTable[x1][y1 - 1] == 0 && virtueTable[x1 - 1][y1] == 0)
                    {
                        bestmoveX = x - 1;
                        bestmoveY = y - 1;
                        x = bestmoveX;
                        y = bestmoveY;
                        return true;
                    }
                }
            }
            if (x == 3 && y == 1)
            {
                if (virtueTable[x - 1][y - 1] < 0)
                {
                    int x1 = (x - 1);
                    int y1 = (y - 1);
                    if (virtueTable[x1 - 1][y1] == 0)
                    {
                        bestmoveX = x - 1;
                        bestmoveY = y - 1;
                        x = bestmoveX;
                        y = bestmoveY;
                        return true;
                    }
                }
            }

            if (x == 2 && y == 1)
            {
                if (virtueTable[x - 1][y - 1] < 0)
                {
                    int x1 = (x - 1);
                    int y1 = (y - 1);
                    if (virtueTable[x1 - 1][y1] == 0)
                    {
                        bestmoveX = x - 1;
                        bestmoveY = y - 1;
                        x = bestmoveX;
                        y = bestmoveY;
                        return true;
                    }
                }
            }
        }

        //0731 副对角线取消掉定式处理
        if (whoplay <= 10 && num1 == 1 && ((x == 2 && y == 3) || (x == 2 && y == 4) || (x == 3 && y == 2) || (x == 4 && y == 2) || (x == 3 && y == 3)))
        {
            if (virtueTable[x - 1][y] < 0)
            {
                bestmoveX = x - 1;
                bestmoveY = y;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (virtueTable[x - 1][y - 1] < 0)
            {
                bestmoveX = x - 1;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (virtueTable[x][y - 1] < 0)
            {
                bestmoveX = x;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
        }
        //0801

        //0801
        if (whoplay >= 8 && ((x == 2 && y == 1) || (x == 1 && y == 2)) && ((virtueTable[0][0] < 0 && virtueTable[1][0] < 0) || (virtueTable[0][0] < 0 && virtueTable[0][1] < 0)) && (!(virtueTable[4][3] < 0 || virtueTable[3][3] < 0 || virtueTable[3][4] < 0)))
        { //qDebug()<<123456;
            bestmoveX = x - 1;
            bestmoveY = y - 1;
            x = bestmoveX;
            y = bestmoveY;
            return true;
        }
        /*if(whoplay>=10)
      {   int num_red=0;
          for(int i=0;i<5;++i)
          {
              for(int j=0;j<5;++j)
              {

              }
          }
      }*/
        //0801 定式处理
        if (num1 == 0 && ((x == 2 && y == 4) || (x == 4 && y == 2)))
        {
            bestmoveX = x - 1;
            bestmoveY = y - 1;
            x = bestmoveX;
            y = bestmoveY;
            return true;
        }
        if (x == 1 && y == 1)
        {
            bestmoveX = x - 1;
            bestmoveY = y - 1;
            x = bestmoveX;
            y = bestmoveY;
            return true;
        }

        if (sente==1 && whoplay == 1)
        {
            if (x == 4 && y == 3)
            {
                bestmoveX = x;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (x == 3 && y == 4)
            {
                bestmoveX = x - 1;
                bestmoveY = y;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (x == 4 && y == 4)
            {
                bestmoveX = x - 1;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (x == 3 && y == 3)
            {
                bestmoveX = x - 1;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (x == 2 && y == 4)
            {
                bestmoveX = x - 1;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (x == 4 && y == 2)
            {
                bestmoveX = x - 1;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
        }
        if (sente==1 && whoplay == 0)
        {
            if (x == 4 && y == 3)
            {
                bestmoveX = x;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (x == 3 && y == 4)
            {
                bestmoveX = x - 1;
                bestmoveY = y;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (x == 4 && y == 4)
            {
                bestmoveX = x - 1;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (x == 3 && y == 3)
            {
                bestmoveX = x - 1;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (x == 2 && y == 4)
            {
                bestmoveX = x - 1;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
            if (x == 4 && y == 2)
            {
                bestmoveX = x - 1;
                bestmoveY = y - 1;
                x = bestmoveX;
                y = bestmoveY;
                return true;
            }
        }
    }
    return false;
}


float Logic::blueMin(int x, int y, int depth, float alpha, float beta)
{

    //胜负已定
    //判断输赢打印信息
    if (judgeResult() == 1)
    {
        return -infinity;
    }
    if (judgeResult() == 2)
    {
        return infinity;
    }

    int a2 = 0;
    float val = 0, temp = 0;

    if (depth == 0)
    {
        if (x > 0 && y > 0)//有左上方
        {
            //遍历三个方向寻求value()最大值
            //qDebug()<<"BlueMin "<<depth<<":3";
            //左上
            a2 = virtueTable[x - 1][y - 1];
            virtueTable[x - 1][y - 1] = virtueTable[x][y];
            virtueTable[x][y] = 0;
            val = value();
            virtueTable[x][y] = virtueTable[x - 1][y - 1];
            virtueTable[x - 1][y - 1] = a2;
            //Alpha剪枝
            beta = qMin(beta, val);
            if (beta <= alpha)
                return beta;

           //左边
            a2 = virtueTable[x - 1][y];
            virtueTable[x - 1][y] = virtueTable[x][y];
            virtueTable[x][y] = 0;
            temp = value();
            virtueTable[x][y] = virtueTable[x - 1][y];
            if (temp < val)
            {
                val = temp;
            }
            virtueTable[x - 1][y] = a2;
             //Alpha剪枝
            beta = qMin(beta, val);
            if (beta <= alpha)
                return beta;

             //上方
            a2 = virtueTable[x][y - 1];
            virtueTable[x][y - 1] = virtueTable[x][y];
            virtueTable[x][y] = 0;
            temp = value();
            virtueTable[x][y] = virtueTable[x][y - 1];
            if (temp < val)
            {
                val = temp;
            }
            virtueTable[x][y - 1] = a2;
            //Alpha剪枝
            beta = qMin(beta, val);
            if (beta <= alpha)
                return beta;
        }
        else if (x == 0)
        {
            //qDebug()<<"BlueqMin "<<depth<<":1";
            a2 = virtueTable[x][y - 1];
            virtueTable[x][y - 1] = virtueTable[x][y];
            virtueTable[x][y] = 0;
            val = value();
            virtueTable[x][y] = virtueTable[x][y - 1];
            virtueTable[x][y - 1] = a2;
        }
        else if (y == 0)
        {
            //qDebug()<<"BlueqMin "<<depth<<":1";
            a2 = virtueTable[x - 1][y];
            virtueTable[x - 1][y] = virtueTable[x][y];
            virtueTable[x][y] = 0;
            val = value();
            virtueTable[x][y] = virtueTable[x - 1][y];
            virtueTable[x - 1][y] = a2;
        }
        return val;
    }

    if (x > 0 && y > 0) //鏈夊乏涓婃柟
    {
        //遍历三个方向寻求value()最大值
        //qDebug()<<"BlueqMin "<<depth<<":3";
        //蓝棋走左上--------------------------------------------------------
        a2 = virtueTable[x - 1][y - 1];
        virtueTable[x - 1][y - 1] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //计算左边价值
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] < 0)
                {
                    //BlueProbability ();
                    redReady();
                    val += redProbability[-virtueTable[i][j] - 1] * redMax(i, j, /*num,*/ depth - 1, alpha, beta);
                }
        //最优棋步
        virtueTable[x][y] = virtueTable[x - 1][y - 1];
        virtueTable[x - 1][y - 1] = a2;
        //Alpha鍓灊
        beta = qMin(beta, val);
        if (beta <= alpha)
            return beta;

         //蓝棋走左边--------------------------------------------------------
        a2 = virtueTable[x - 1][y];
        virtueTable[x - 1][y] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //计算左边价值
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] < 0)
                {
                    //BlueProbability ();
                    redReady();
                    temp += redProbability[-virtueTable[i][j] - 1] * redMax(i, j, /*num,*/ depth - 1, alpha, beta);
                }
         //最优棋步
        if (temp < val)
        {
            val = temp;
        }
        temp = 0;
        //最优棋步
        virtueTable[x][y] = virtueTable[x - 1][y];
        virtueTable[x - 1][y] = a2;
        //Alpha剪枝
        beta = qMin(beta, val);
        if (beta <= alpha)
            return beta;

       //蓝棋走上方--------------------------------------------------------
        a2 = virtueTable[x][y - 1];
        virtueTable[x][y - 1] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //计算上方价值
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] < 0)
                {
                    //BlueProbability ();
                    redReady();
                    temp += redProbability[-virtueTable[i][j] - 1] * redMax(i, j, /*num,*/ depth - 1, alpha, beta);
                }
       //最优棋步
        if (temp < val)
        {
            val = temp;
        }
        //鎭㈠妫嬬洏
        virtueTable[x][y] = virtueTable[x][y - 1];
        virtueTable[x][y - 1] = a2;
        //Alpha鍓灊
        beta = qMin(beta, val);
        if (beta <= alpha)
            return beta;
    }
    else if (x == 0)
    {
        //qDebug()<<"BlueqMin "<<depth<<":1";
        //钃濇璧颁笂鏂-------------------------------------------------------
        a2 = virtueTable[x][y - 1];
        virtueTable[x][y - 1] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //璁＄畻涓婃柟浠峰€
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] < 0)
                {
                    //BlueProbability ();
                    redReady();
                    val += redProbability[-virtueTable[i][j] - 1] * redMax(i, j, /*num,*/ depth - 1, alpha, beta);
                }
        //鎭㈠妫嬬洏
        virtueTable[x][y] = virtueTable[x][y - 1];
        virtueTable[x][y - 1] = a2;
    }
    else if (y == 0)
    {
        //qDebug()<<"BlueqMin "<<depth<<":1";
        //蓝棋走上方--------------------------------------------------------
        a2 = virtueTable[x - 1][y];
        virtueTable[x - 1][y] = virtueTable[x][y];
        virtueTable[x][y] = 0;
          //计算上方价值
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] < 0)
                {
                    //BlueProbability ();
                    redReady();
                    val += redProbability[-virtueTable[i][j] - 1] * redMax(i, j, /*num,*/ depth - 1, alpha, beta);
                }
        //恢复棋盘
        virtueTable[x][y] = virtueTable[x - 1][y];
        virtueTable[x - 1][y] = a2;
    }
    return val;
}

float Logic::redMax(int x, int y, int depth, float alpha, float beta)
{
    if (judgeResult() == 1)
    {
        return -infinity;
    }
    if (judgeResult() == 2)
    {
        return infinity;
    }

    //胜负已定
    //判断输赢打印信息
    if (judgeResult() == 1)
    {
        return -infinity;
    }
    if (judgeResult() == 2)
    {
        return infinity;
    }

    int a;
    float val = 0, temp = 0;

    if (depth == 0) //已经达到最深度
    {
        if (x < 4 && y < 4) ///有右下方,这样
        {
            //遍历三个方向寻求value()最大值
            //qDebug()<<"RedMax "<<depth<<":3";


            /*****************右下**************/

            /*********先模拟走一步*******/
            a = virtueTable[x + 1][y + 1];
            virtueTable[x + 1][y + 1] = virtueTable[x][y];
            virtueTable[x][y] = 0;
            val = value(); //计算当前的估值函数
            /*********先模拟走一步*******/

            /******撤出模拟状态*******/
            virtueTable[x][y] = virtueTable[x + 1][y + 1];
            virtueTable[x + 1][y + 1] = a;
            /******撤出模拟状态*******/
            //Beta剪枝
            alpha = qMax(alpha, val);
            if (beta <= alpha)
                return alpha;


            /*****************右下**************/


            /*****************右***************/
            a = virtueTable[x + 1][y];
            virtueTable[x + 1][y] = virtueTable[x][y];
            virtueTable[x][y] = 0;
            temp = value();
            virtueTable[x][y] = virtueTable[x + 1][y];
            if (temp > val)
            {
                val = temp;
            }
            virtueTable[x + 1][y] = a;
            //Beta剪枝
            alpha = qMax(alpha, val);
            if (beta <= alpha)
                return alpha;
            /*****************右***************/


            /****************下***************/
            a = virtueTable[x][y + 1];
            virtueTable[x][y + 1] = virtueTable[x][y];
            virtueTable[x][y] = 0;
            temp = value();
            virtueTable[x][y] = virtueTable[x][y + 1];
            if (temp > val)
            {
                val = temp;
            }
            virtueTable[x][y + 1] = a;
            //Beta剪枝
            alpha = qMax(alpha, val);
            if (beta <= alpha)
                return alpha;
            /****************下***************/
        }
        else if (x == 4)
        {
            /****************下***************/
            //qDebug()<<"RedMax "<<depth<<":1";
            a = virtueTable[x][y + 1];
            virtueTable[x][y + 1] = virtueTable[x][y];
            virtueTable[x][y] = 0;
            val = value();
            virtueTable[x][y] = virtueTable[x][y + 1];
            virtueTable[x][y + 1] = a;
             /****************下***************/
        }
        else if (y == 4)
        {
             /***********右*****************/
            //qDebug()<<"RedMax "<<depth<<":1";
            a = virtueTable[x + 1][y];
            virtueTable[x + 1][y] = virtueTable[x][y];
            virtueTable[x][y] = 0;
            val = value();
            virtueTable[x][y] = virtueTable[x + 1][y];
            virtueTable[x + 1][y] = a;
             /***********右*****************/
        }
        return val; //鍥犱负鍒拌竟鐣屼笂鍙湁涓€鏉¤矾鍙蛋锛屾墍浠ヨ鐩存帴杩斿洖val
    }




    //杩樻病鏈夎揪鍒版渶娣卞害
    if (x < 4 && y < 4) //鏈夊彸涓嬫柟
    {
        //遍历三个方向寻求value()最大值
        //qDebug()<<"RedMax "<<depth<<":3";
        //红棋走右下--------------------------------------------------------
        a = virtueTable[x + 1][y + 1];
        a = virtueTable[x + 1][y + 1];
        virtueTable[x + 1][y + 1] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //璁＄畻鍙充笅鐐逛环鍊
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] > 0)
                {
                    blueReady(); //get blueprobability,and update the values of chess
                    val += blueProbability[virtueTable[i][j] - 1] * blueMin(i, j, depth - 1, alpha, beta);
                }


        //鎭㈠妫嬬洏
        virtueTable[x][y] = virtueTable[x + 1][y + 1];
        virtueTable[x + 1][y + 1] = a;
        //Beta鍓灊
        alpha = qMax(alpha, val);
        if (beta <= alpha)
            return alpha;

        //绾㈡璧板彸杈-------------------------------------------------------
        a = virtueTable[x + 1][y];
        virtueTable[x + 1][y] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //璁＄畻宸﹁竟浠峰€
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] > 0)
                {
                    blueReady();
                    //RedProbability ();
                    temp += blueProbability[virtueTable[i][j] - 1] * blueMin(i, j, /*num,*/ depth - 1, alpha, beta);
                }
        //鏈€浼樻姝
        if (temp > val)
        {
            val = temp;
        }
        temp = 0;
        //鎭㈠妫嬬洏
        virtueTable[x][y] = virtueTable[x + 1][y];
        virtueTable[x + 1][y] = a;
        //Beta鍓灊
        alpha = qMax(alpha, val);
        if (beta <= alpha)
            return alpha;

        //绾㈡璧颁笅鏂-------------------------------------------------------
        a = virtueTable[x][y + 1];
        virtueTable[x][y + 1] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //璁＄畻涓婃柟浠峰€
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] > 0)
                {
                    blueReady();
                    //RedProbability ();
                    temp += blueProbability[virtueTable[i][j] - 1] * blueMin(i, j, /*num,*/ depth - 1, alpha, beta);
                }
        //鏈€浼樻姝
        if (temp > val)
        {
            val = temp;
        }
        //鎭㈠妫嬬洏
        virtueTable[x][y] = virtueTable[x][y + 1];
        virtueTable[x][y + 1] = a;
        //Beta鍓灊
        alpha = qMax(alpha, val);
        if (beta <= alpha)
            return alpha;
    }
    else if (x == 4)
    {
        //qDebug()<<"RedMax "<<depth<<":1";
        //绾㈡璧颁笅鏂-------------------------------------------------------
        a = virtueTable[x][y + 1];
        virtueTable[x][y + 1] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //璁＄畻涓婃柟浠峰€
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] > 0)
                {
                    blueReady();
                    //RedProbability ();
                    val += blueProbability[virtueTable[i][j] - 1] * blueMin(i, j, /*num,*/ depth - 1, alpha, beta);
                }
        //鎭㈠妫嬬洏
        virtueTable[x][y] = virtueTable[x][y + 1];
        virtueTable[x][y + 1] = a;
    }
    else if (y == 4)
    {
        //qDebug()<<"RedMax "<<depth<<":3";
        //绾㈡璧板彸杈-------------------------------------------------------
        a = virtueTable[x + 1][y];
        virtueTable[x + 1][y] = virtueTable[x][y];
        virtueTable[x][y] = 0;
        //璁＄畻宸﹁竟浠峰€
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (virtueTable[i][j] > 0)
                {
                    blueReady();
                    //RedProbability ();
                    val += blueProbability[virtueTable[i][j] - 1] * blueMin(i, j, /*num,*/ depth - 1, alpha, beta);
                }
        //鎭㈠妫嬬洏
        virtueTable[x][y] = virtueTable[x + 1][y];
        virtueTable[x + 1][y] = a;
    }

    return val;
}

float Logic::value()
{
    float bluedistance = 0;
    float reddistance = 0;
    float blueThreaten = 0;
    float redThreaten = 0;
    float val = 0;

    blueReady(); //得到了蓝红双方的价值以及蓝方的个体威胁值
    for (int i = 0; i < SIZE; i++){
        if (qAbs(blueProbability[i]-0.00f) > 0.005) //棋子存在
        {
            bluedistance += blueProbability[i] * blueValue[i]; //我方进攻值
            blueThreaten+= blueProbability[i] * bluethreaten[i];
        }
    }
    // 蓝方的威胁值



    redReady();
    for (int i = 0; i < SIZE; i++){
        if (qAbs(redProbability[i]-0.00f) > 0.005){ //妫嬪瓙瀛樺湪
            reddistance += redProbability[i] * redValue[i]; //绾㈡柟杩涙敾鍊
            redThreaten += redProbability[i] * redthreaten[i];
        }
    }
    //绾㈡柟鐨勫▉鑳佸€

    val = (k1 * reddistance + k2 * bluedistance + k3 * blueThreaten + k4 * redThreaten); /**/


    return val;
}

\

void Logic::blueReady()
{
    QVector<int> bluedistancerate(SIZE,0);

    for (int i = 0; i < LINE; i++){
        blueProbability[i] = 0;
    }
    for (int i = 0; i < LINE; i++){
        for (int j = 0; j < 2; j++){
            blueprobabilityflag[i][j] = false;
        }
    }
    for (int i = 0; i < LINE; i++){
        redValue[i] = 0;
    }
    for (int i = 0; i < LINE; i++){
        blueValue[i] = 0;
    }
    for (int i = 0; i < LINE; i++){
        bluethreaten[i] = 0;
    }


    for (int i=0;i<LINE;i++) {
        for (int j=0;j<LINE;j++) {
            if(virtueTable[i][j]>0){
                blueValue[virtueTable[i][j]-1]=blueValueChart[i][j];
            }
            else if(virtueTable[i][j]<0){
                redValue[-virtueTable[i][j]-1]=redValueChart[i][j];
            }
        }
    }


    for (int i=0;i<LINE;i++) {
        for (int j=0;j<LINE;j++) {
            if(virtueTable[i][j]>0){
                if(i!=0 && j!=0){
                    blueprobabilityflag[virtueTable[i][j] - 1][0] = true;
                    int a = 0, b = 0, c = 0, temp;

                    if (virtueTable[i][j - 1] < 0){
                        a = redValue[-virtueTable[i][j-1] - 1];
                    }
                    if (virtueTable[i - 1][j - 1] < 0){
                        b = redValue[-virtueTable[i-1][j-1] - 1];
                    }
                    if (virtueTable[i - 1][j] < 0){
                        c = redValue[-virtueTable[i-1][j] - 1];
                    }

                    temp = qMax(a,b);
                    temp = qMax(temp, c);
                    bluethreaten[virtueTable[i][j] - 1] = temp;
                }

                else if (i==0&&j!=0) {
                    blueprobabilityflag[virtueTable[i][j] - 1][0] = true;
                    int temp=0;
                    if(virtueTable[i][j-1]<0){
                        temp=redValue[-virtueTable[i][j-1]-1];
                    }
                    bluethreaten[virtueTable[i][j] - 1]=temp;
                }

                else if(i!=0&&j==0){
                    blueprobabilityflag[virtueTable[i][j] - 1][0] = true;
                    int temp=0;
                    if(virtueTable[i-1][j]<0){
                        temp=blueValue[-virtueTable[i-1][j]-1];
                    }
                    bluethreaten[virtueTable[i][j] - 1]=temp;
                }

            }
        }
    }

    int distancerate = 0; //浼樺厛绾
    for (int i = 0; i < 5; i++)
    {
        for (int k = 0; k <= i; k++)
            if (virtueTable[i][k] > 0)
                bluedistancerate[distancerate++] = virtueTable[i][k];
        for (int k = i; k > 0; k--)
            if (virtueTable[k - 1][i] > 0)
                bluedistancerate[distancerate++] = virtueTable[k - 1][i];
    }


    int num=0, sum = 0;
    for (int i = 0; i < 6; i++)
    {
        if (bluedistancerate[i] > 0)
        {
            num = bluedistancerate[i] - 1;
            while (num > 0 && blueprobabilityflag[--num][0] == false && blueprobabilityflag[num][1] == false)
            {
                sum++;
                blueprobabilityflag[num][1] = true; //姒傜巼鏍囧織浣嶇疆1琛ㄧず宸茬粡璁＄畻杩囨鐜囦簡
            }
            num = bluedistancerate[i] - 1;
            while (num < 5 && blueprobabilityflag[++num][0] == false && blueprobabilityflag[num][1] == false)
            {
                sum++;
                blueprobabilityflag[num][1] = true; //姒傜巼鏍囧織浣嶇疆1琛ㄧず宸茬粡璁＄畻杩囨鐜囦簡
            }
            num = bluedistancerate[i] - 1;
            sum++;                           //鍔犱笂鑷韩鐨勬鐜
            blueprobabilityflag[num][1] = true; //鑷韩鏍囧織浣嶇疆1

            blueProbability[num] = sum / 6.0f; //瀛樺偍姒傜巼
            sum = 0;
        }
    }
}



void Logic::redReady()
{
    QVector<int> reddistancerate(SIZE,0);

    for (int i = 0; i < LINE; i++){
        redProbability[i] = 0;
    }
    for (int i = 0; i < LINE; i++){
        for (int j = 0; j < 2; j++){
            redprobabilityflag[i][j] = false;
        }
    }
    for (int i = 0; i < LINE; i++){
        redValue[i] = 0;
    }
    for (int i = 0; i < LINE; i++){
        blueValue[i] = 0;
    }
    for (int i = 0; i < LINE; i++){
        redthreaten[i] = 0;
    }


    for (int i=0;i<LINE;i++) {
        for (int j=0;j<LINE;j++) {
            if(virtueTable[i][j]>0){
                blueValue[virtueTable[i][j]-1]=blueValueChart[i][j];
            }
            else if(virtueTable[i][j]<0){
                redValue[-virtueTable[i][j]-1]=redValueChart[i][j];
            }
        }
    }


    for (int i=0;i<LINE;i++) {
        for (int j=0;j<LINE;j++) {
            if(virtueTable[i][j]<0){
                if(i!=4 && j!=4){
                    redprobabilityflag[-virtueTable[i][j] - 1][0] = true;
                    int a = 0, b = 0, c = 0, temp;

                    if (virtueTable[i][j + 1] > 0)
                        a = blueValue[virtueTable[i][j+1] - 1];
                    if (virtueTable[i + 1][j + 1] > 0)
                        b = blueValue[virtueTable[i+1][j+1] - 1];
                    if (virtueTable[i + 1][j] > 0)
                        c = blueValue[virtueTable[i+1][j] - 1];

                    temp = qMax(a,b);
                    temp = qMax(temp, c);
                    redthreaten[-virtueTable[i][j] - 1] = temp;
                }

                else if (i==4&&j!=4) {
                    redprobabilityflag[-virtueTable[i][j] - 1][0] = true;
                    int temp=0;
                    if(virtueTable[i][j+1]>0){
                        temp=blueValue[virtueTable[i][j+1]-1];
                    }
                    redthreaten[-virtueTable[i][j] - 1]=temp;
                }

                else if(i!=4&&j==4){
                    redprobabilityflag[-virtueTable[i][j] - 1][0] = true;
                    int temp=0;
                    if(virtueTable[i+1][j]>0){
                        temp=blueValue[virtueTable[i+1][j]-1];
                    }
                    redthreaten[-virtueTable[i][j] - 1]=temp;
                }

            }
        }
    }

    int distancerate = 0; //浼樺厛绾
    for (int i = LINE-1; i >= 0; i--){
        for (int k = LINE-1; k >= i; k--){
            if (virtueTable[i][k] < 0){
                reddistancerate[distancerate++] = virtueTable[i][k];
            }
        }
        for (int k = i; k < LINE-1; k++){
            if (virtueTable[k + 1][i] < 0){
                reddistancerate[distancerate++] = virtueTable[k + 1][i];
            }
        }
    }


    int num=0, sum = 0;
    for (int i = 0; i < SIZE; i++) {//6涓瀛愪緷鐓т紭鍏堢骇鍗犻姒傜巼
        if (reddistancerate[i] < 0)
        {
            num = -reddistancerate[i] - 1;
            while (num > 0 && redprobabilityflag[--num][0] == false && redprobabilityflag[num][1] == false)
            {
                sum++;
                redprobabilityflag[num][1] = true; //姒傜巼鏍囧織浣嶇疆1琛ㄧず宸茬粡璁＄畻杩囨鐜囦簡
            }
            num = -reddistancerate[i] - 1;
            while (num < LINE && redprobabilityflag[++num][0] == false && redprobabilityflag[num][1] == false)
            {
                sum++;
                redprobabilityflag[num][1] = true; //姒傜巼鏍囧織浣嶇疆1琛ㄧず宸茬粡璁＄畻杩囨鐜囦簡
            }
            num = -reddistancerate[i] - 1;
            sum++;                          //鍔犱笂鑷韩鐨勬鐜
            redprobabilityflag[num][1] = true; //鑷韩鏍囧織浣嶇疆1

            redProbability[num] = sum / 6.0f; //瀛樺偍姒傜巼
            sum = 0;
        }
    }


}



QVector<QPoint> Logic::getPointToGo()
{
    if(direction==1){
        QVector<QPoint> returnData(2);
        for (int i=0;i<LINE;i++) {
            for (int j=0;j<LINE;j++) {
                if(virtueTable[i][j]==random){
                    returnData[0] = QPoint(i,j);
                    returnData[1] = blueWhereToGo(i,j,depth,-infinity,infinity);
                    return returnData;
                }
            }
        }
        int temp1 = 0; //鐢ㄤ簬淇濆瓨灏忎簬randnum涓旀渶鎺ヨ繎鐨
        int temp2 = 7; //鐢ㄤ簬淇濆瓨澶т簬randnum涓旀渶鎺ヨ繎鐨
        int k1, l1;
        int k2, l2;

        for (int k = 0; k < 5; ++k){
            for (int l = 0; l < 5; ++l)
            {
                if (virtueTable[k][l] > temp1 && virtueTable[k][l] < random) //灏忎簬randnum涓旀渶鎺ヨ繎鐨
                {
                    temp1 = virtueTable[k][l];
                    k1 = k;
                    l1 = l;
                }
                else if (virtueTable[k][l] > random && virtueTable[k][l] < temp2)
                {
                    temp2 = virtueTable[k][l];
                    k2 = k;
                    l2 = l;
                }
            }
        }

        if (temp1 != 0 && temp2 == 7)
        {
            //澶囦唤妫嬬洏锛岀敤浜庢倲妫
            returnData[0] = QPoint(k1,l1);
            returnData[1] = blueWhereToGo(k1,l1,depth,-infinity,infinity);
            return returnData;
        }
        else if (temp1 == 0 && temp2 != 7)
        {
            //澶囦唤妫嬬洏锛岀敤浜庢倲妫
            returnData[0] = QPoint(k2,l2);
            returnData[1] = blueWhereToGo(k2,l2,depth,-infinity,infinity);
            return returnData;
        }
        else
        {
            float value1 = blueMin(k1, l1, depth, -infinity, infinity);
            float value2 = blueMin(k2, l2, depth, -infinity, infinity);
            if (value1 > value2) //璇ヨ蛋k2,l2瀵瑰簲鐨勬瀛
            {
                returnData[0] = QPoint(k2,l2);
                returnData[1] = blueWhereToGo(k2,l2,depth,-infinity,infinity);
                return returnData;
            }
            else
            {
                //璧版
                returnData[0] = QPoint(k1,l1);
                returnData[1] = blueWhereToGo(k1,l1,depth,-infinity,infinity);
                return returnData;
            }
        }
    }
    else if(direction==-1){
        QVector<QPoint> returnData(2);
        for (int i=0;i<LINE;i++) {
            for (int j=0;j<LINE;j++) {
                if(virtueTable[i][j]==random){
                    returnData[0] = QPoint(4-j,4-i);
                    returnData[1] = blueWhereToGo(i,j,depth,-infinity,infinity);
                    int temp=4-returnData[1].x();
                    returnData[1].setX(4-returnData[1].y());
                    returnData[1].setY(temp);
                    return returnData;
                }
            }
        }
        int temp1 = 0; //鐢ㄤ簬淇濆瓨灏忎簬randnum涓旀渶鎺ヨ繎鐨
        int temp2 = 7; //鐢ㄤ簬淇濆瓨澶т簬randnum涓旀渶鎺ヨ繎鐨
        int k1, l1;
        int k2, l2;

        for (int k = 0; k < 5; ++k){
            for (int l = 0; l < 5; ++l)
            {
                if (virtueTable[k][l] > temp1 && virtueTable[k][l] < random) //灏忎簬randnum涓旀渶鎺ヨ繎鐨
                {
                    temp1 = virtueTable[k][l];
                    k1 = k;
                    l1 = l;
                }
                else if (virtueTable[k][l] > random && virtueTable[k][l] < temp2)
                {
                    temp2 = virtueTable[k][l];
                    k2 = k;
                    l2 = l;
                }
            }
        }

        if (temp1 != 0 && temp2 == 7)
        {
            //澶囦唤妫嬬洏锛岀敤浜庢倲妫
            returnData[0] = QPoint(4-l1,4-k1);
            returnData[1] = blueWhereToGo(k1,l1,depth,-infinity,infinity);
            int temp=4-returnData[1].x();
            returnData[1].setX(4-returnData[1].y());
            returnData[1].setY(temp);
            return returnData;
        }
        else if (temp1 == 0 && temp2 != 7)
        {
            //澶囦唤妫嬬洏锛岀敤浜庢倲妫
            returnData[0] = QPoint(4-l2,4-k2);
            returnData[1] = blueWhereToGo(k2,l2,depth,-infinity,infinity);
            int temp=4-returnData[1].x();
            returnData[1].setX(4-returnData[1].y());
            returnData[1].setY(temp);
            return returnData;
        }
        else
        {
            float value1 = blueMin(k1, l1, depth, -infinity, infinity);
            float value2 = blueMin(k2, l2, depth, -infinity, infinity);
            if (value1 > value2) //璇ヨ蛋k2,l2瀵瑰簲鐨勬瀛
            {
                returnData[0] = QPoint(4-l2,4-k2);
                returnData[1] = blueWhereToGo(k2,l2,depth,-infinity,infinity);
                int temp=4-returnData[1].x();
                returnData[1].setX(4-returnData[1].y());
                returnData[1].setY(temp);
                return returnData;
            }
            else
            {
                //璧版
                returnData[0] = QPoint(4-l1,4-k1);
                returnData[1] = blueWhereToGo(k1,l1,depth,-infinity,infinity);
                int temp=4-returnData[1].x();
                returnData[1].setX(4-returnData[1].y());
                returnData[1].setY(temp);
                return returnData;
            }
        }
    }

}



void Logic::setvirtueTable(const QVector<QVector<int> > &board)
{
    if(direction==1){
        for (int i=0;i<LINE;i++) {
            for (int j=0;j<LINE;j++) {
                virtueTable[i][j]=board[i][j];
            }
        }
    }
    else if (direction==-1) {
        for (int i=0;i<LINE;i++) {
            for (int j=0;j<LINE;j++) {
                virtueTable[i][j]=-board[4-j][4-i];
            }
        }


    }


}

void Logic::setRand(int rand){
    this->random=rand;
}//鑾峰彇楠板瓙鏁
void Logic::setDepth(int depth){
    this->depth=depth;
}
void Logic::setSente(int sente){
    this->sente=sente;
}
void Logic::setourColor(int ourColor){
    this->direction=ourColor;
}



namespace py = boost::python;



py::list get_move(py::list board, int point, int depth, int sente, int ourColor)
{
    std::cout << "poin"<<point << std::endl;
    std::cout << "depth"<<depth << std::endl;
    std::cout << "sente"<<sente << std::endl;
    std::cout << "ourColor"<<ourColor << std::endl;

    QVector<QVector<int> > board_;
    for (int i = 0; i < 5; i++)
    {
        py::list row = py::extract<py::list>(board[i]);
        QVector<int> row_;
        for (int j = 0; j < 5; j++)
        {
            row_.push_back(py::extract<int>(row[j]));
            std::cout << row_[j] << " ";
        }
        std::cout << std::endl;
        board_.push_back(row_);
    }
    Logic logic;
    logic.setvirtueTable(board_);
    logic.setRand(point);
    logic.setDepth(depth);
    logic.setSente(sente);
    logic.setourColor(ourColor);
    QVector<QPoint> move = logic.getPointToGo();
    py::list result;
    result.append(move[0].x());
    result.append(move[0].y());
    result.append(move[1].x());
    result.append(move[1].y());
    return result;
}


BOOST_PYTHON_MODULE(logic)
{
    py::def("get_move", get_move);

}

