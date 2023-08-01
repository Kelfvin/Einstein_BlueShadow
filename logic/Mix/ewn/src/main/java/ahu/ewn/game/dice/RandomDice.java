package ahu.ewn.game.dice;

import java.util.Random;

/**
 * 随机骰子策略，从1~6中随机生成一个骰子点数
 */
public class RandomDice extends Dice {

    public RandomDice(){
        super();
        setLabel("RandomDice");
    }

    @Override
    public byte getDice() {
        Random random = new Random();
        return (byte)(random.nextInt(6)+1);
    }
}
