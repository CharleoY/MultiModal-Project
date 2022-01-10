package com.samborskiy.entity.analyzers.frequency;

import com.samborskiy.entity.PartOfSpeech;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

/**
 * Frequency analyzer based on dictionary.
 */
public class FrequencyDictionary extends FrequencyAnalyzer {

    private static final double DEFAULT_FREQUENCY = 1.;
    private static final String DEFAULT_DICTIONARY_PATH = "res/ru/lemma.al";
    private final Map<String, WordFrequency> words = new HashMap<>();

    public FrequencyDictionary() {
        this(DEFAULT_DICTIONARY_PATH);
    }

    public FrequencyDictionary(String filePath) {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), "UTF-8"))) {
            reader.readLine(); // skip meta info line
            String line;
            while ((line = reader.readLine()) != null) {
                StringTokenizer tokenizer = new StringTokenizer(line);
                tokenizer.nextToken(); // skip number of word in alphabetical order
                double frequency = Double.parseDouble(tokenizer.nextToken());
                String word = tokenizer.nextToken();
                String partOfSpeech = tokenizer.nextToken();
                words.put(word, new WordFrequency(frequency, word, partOfSpeech));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public double getFrequency(String word) {
        if (words.containsKey(word)) {
            return words.get(word).getFrequency();
        } else {
            return DEFAULT_FREQUENCY;
        }
    }

    public PartOfSpeech getPartOfSpeech(String word) {
        if (words.containsKey(word)) {
            return words.get(word).getPartOfSpeech();
        } else {
            return null;
        }
    }
}
