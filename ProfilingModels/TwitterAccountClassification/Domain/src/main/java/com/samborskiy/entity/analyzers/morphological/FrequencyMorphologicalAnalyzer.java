package com.samborskiy.entity.analyzers.morphological;

import com.samborskiy.entity.PartOfSpeech;
import com.samborskiy.entity.analyzers.frequency.FrequencyDictionary;

/**
 * Morphological analyzer based on frequency dictionary.
 *
 * @author Whiplash
 */
public class FrequencyMorphologicalAnalyzer extends MorphologicalAnalyzer {

    private final FrequencyDictionary frequencyDictionary = new FrequencyDictionary();

    @Override
    public PartOfSpeech get(String word) {
        SimpleMorphologicalAnalyzer morphologicalAnalyzer = new SimpleMorphologicalAnalyzer();
        PartOfSpeech partOfSpeech = frequencyDictionary.getPartOfSpeech(word);
        if (partOfSpeech == null) {
            partOfSpeech = morphologicalAnalyzer.get(word);
        }
        return partOfSpeech;
    }
}
