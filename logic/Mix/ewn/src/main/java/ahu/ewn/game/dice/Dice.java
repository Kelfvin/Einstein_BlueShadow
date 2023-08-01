package ahu.ewn.game.dice;

/**
 * 骰子策略基类。调用getDice()生成一个骰子点数
 */
abstract public class Dice {

    /**
     * 标签，策略名称
     */
    protected String label;

    /**
     * 获取一个骰子点数
     *
     * @return 骰子点数
     */
    abstract public byte getDice();

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
