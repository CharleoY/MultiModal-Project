package com.samborskiy.entity;

public class Log {

    private Log() {
    }

    public static void d(String text) {
        if (ClassifierProperty.isDebug()) {
            System.out.println(text);
        }
    }

    public static void e(String text) {
        System.err.println(text);
    }

    public static void e(String text, Throwable e) {
        System.err.println(text);
        e.printStackTrace();
    }
}
