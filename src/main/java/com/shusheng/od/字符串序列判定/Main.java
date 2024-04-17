package com.shusheng.od.字符串序列判定;

import java.util.Scanner;

public class Main {

    /**
     * 输入：
gao
qwebgshaccoohj
     * 输出： 10
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String shortStr = scanner.nextLine();
        String longStr = scanner.nextLine();
        int find = getFind(shortStr, longStr);
        System.out.println(find);

    }

    public static int getFind(String shortStr, String longStr) {
        int findIndex = 0;
        int find = -1;
        for (int i = 0; i < longStr.length(); i++) {
            char lChar = longStr.charAt(i);
            char sChar = shortStr.charAt(findIndex);
            if (lChar == sChar) {
                findIndex++;
            }
            // 中止条件
            if (findIndex== shortStr.length()){
                find = i;
                break;
            }
        }
        return find;
    }

}
