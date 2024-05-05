package com.shusheng.od.数组;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;

import javax.imageio.stream.FileImageInputStream;

public class AgeStas {

	public static void main(String[] args) throws Exception {
		String str = null;
		String fileName = "d:\\age1.txt";
		InputStreamReader isr = new InputStreamReader(new FileInputStream(fileName),"UTF-8");
		
		long start = System.currentTimeMillis();
		BufferedReader br = new BufferedReader(isr);
		int tot = 0 ;	//21亿
		int data [] = new int[200];
		while((str = br.readLine()) != null){		//一行一行的读 O(n)
			int age = Integer.valueOf(str);
			data[age] ++ ;
			tot ++ ;
		}
		//O(n) 14亿. 100万/秒 *1000 = 10亿 100~1000s之间 => 500s以下 60*8=480s
		System.out.println("总共的数据大小: " + tot);
		
		for(int i = 0 ; i < 200 ; i ++){//下标从0开始的
			System.out.println(i + ":" + data[i]);
		}
		//144239ms => 144s
		System.out.println("计算花费的时间为:" + (System.currentTimeMillis() - start) + "ms");
	}
}
