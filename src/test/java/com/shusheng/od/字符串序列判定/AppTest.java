package com.shusheng.od.字符串序列判定;

import static com.shusheng.od.字符串序列判定.Main.getFind;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

/**
 * Unit test for simple App.
 */
public class AppTest 
{
    /**
     * Rigorous Test :-)
     */
    @Test
    public void t1()
    {
        String s = "gao";
        String l = "qwebgshaccoohj";
        int find = getFind(s, l);
        assertTrue( find == 10);
        System.out.println("测试通过");
    }
    @Test
    public void t2()
    {
        String s = "xxx";
        String l = "qwxxebxgsxhaxccoohj";
        int find = getFind(s, l);
        assertTrue( find == 6);
        System.out.println("测试通过");
    }
    @Test
    public void t3()
    {
        String s = "o";
        String l = "oqwxxeboxgsxhaxccoohj";
        int find = getFind(s, l);
        assertTrue( find == 0);
        System.out.println("测试通过");
    }
}
