package com.shusheng.od;

import java.util.Scanner;

public class SumOfNumbers {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 循环读取数据直到没有更多输入
        while (scanner.hasNextLine()) {
            // 读取每行的第一个整数n
            int n = scanner.nextInt();
            int sum = 0;

            // 读取接下来的n个整数并累加
            for (int i = 0; i < n; i++) {
                int val = scanner.nextInt();
                sum += val;
            }

            // 输出该组数据的和
            System.out.println(sum);
        }

        scanner.close();
    }
}
