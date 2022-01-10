package com.samborskiy.extraction.entity;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;

import java.util.HashMap;
import java.util.Map;

/**
 * Enum stores language.
 *
 * @author Whiplash
 */
public enum Language {

    /**
     * Russian language.
     */
    ru,
    /**
     * English language.
     */
    en;

    private static Map<String, Language> strToLang = new HashMap<>(Language.values().length);

    static {
        strToLang.put("ru", ru);
        strToLang.put("en", en);
    }

    // the same as {'А', 'Я', 'а', 'я'};
    private static final int[] RU_RANGES = {1040, 1071, 1072, 1103};
    private static final int[] EN_RANGES = {'A', 'Z', 'a', 'z'};

    /**
     * Creates element of enum class {@code Language} from string {@code value}.
     *
     * @param value string which is obtained from enum
     * @return element of enum class
     */
    @JsonCreator
    public static Language fromString(String value) {
        return strToLang.get(value);
    }

    @JsonValue
    @Override
    public String toString() {
        for (Map.Entry<String, Language> entry : strToLang.entrySet()) {
            if (entry.getValue() == this) {
                return entry.getKey();
            }
        }
        return null;
    }

    /**
     * Checks is this word belongs to this language.
     *
     * @param word word to be checked
     * @return {@code true} if word belongs to this language, {@code false} otherwise
     */
    public boolean isCorrectWord(String word) {
        switch (this) {
            case ru:
                return isCorrectWord(word, RU_RANGES);
            case en:
                return isCorrectWord(word, EN_RANGES);
            default:
                return false;
        }
    }

    /**
     * Checks is every letter of this word in ranges.
     *
     * @param word   word to be checked
     * @param ranges ranges which should contain letters of the word
     * @return {@code true} if every letter of this word in ranges, {@code false} otherwise
     */
    private boolean isCorrectWord(String word, int... ranges) {
        for (int i = 0; i < word.length(); i++) {
            if (!inRange(word.charAt(i), ranges)) {
                return false;
            }
        }
        return true;
    }

    /**
     * Checks is letter in ranges.
     *
     * @param letter letter to be checked
     * @param ranges ranges which should contain letters of the word
     * @return {@code true} if letter in ranges, {@code false} otherwise
     */
    private boolean inRange(char letter, int... ranges) {
        boolean isCorrect = false;
        for (int j = 0; j < ranges.length; j += 2) {
            if (letter >= ranges[j] && letter <= ranges[j + 1]) {
                isCorrect = true;
            }
        }
        return isCorrect;
    }

}
