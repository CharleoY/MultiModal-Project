package com.samborskiy.entity.analyzers.morphological;

import com.samborskiy.entity.PartOfSpeech;

/**
 * Analyzer of morphological characteristics of words.
 *
 * @author Whiplash
 */
public abstract class MorphologicalAnalyzer {

    private static final MorphologicalAnalyzer analyzer = new SimpleMorphologicalAnalyzer();

    /**
     * Returns part of speech of word.
     *
     * @param word word for which will be determined part of speech
     * @return part of speech of word
     */
    public abstract PartOfSpeech get(String word);

    public static MorphologicalAnalyzer get() {
        return analyzer;
    }
}
