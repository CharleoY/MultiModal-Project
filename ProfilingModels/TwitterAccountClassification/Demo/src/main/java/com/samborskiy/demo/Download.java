package com.samborskiy.demo;

import com.samborskiy.extraction.Extractor;

import java.io.File;

public class Download {

    public static void main(String[] args) throws Exception {
        Extractor extractor = new Extractor(new File("../res/en/config.json"));
        extractor.update();
    }
}
