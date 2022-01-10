package com.samborskiy.entity.analyzers.morphological;

import com.samborskiy.entity.PartOfSpeech;

import java.util.*;

import static com.samborskiy.entity.PartOfSpeech.*;

/**
 * Morphological analyzer based on word endings.
 *
 * @author Whiplash
 */
public class SimpleMorphologicalAnalyzer extends MorphologicalAnalyzer {

    private static final Map<PartOfSpeech, List<String>> ENDINGS = new HashMap<>();

    static {
        String[] adjectiveEndings = {"ее", "ие", "ые", "ое", "ими", "ыми", "ей", "ий", "ый", "ой", "ем", "им", "ым", "ом", "его", "ого", "ему", "ому", "их", "ых", "ую", "юю", "ая", "яя", "ою", "ею"};
        String[] communionEndings = {"ивш", "ывш", "ующ", "ем", "нн", "вш", "ющ", "ущи", "ющи", "ящий", "щих", "щие", "ляя"};
        String[] verbEndings = {"ила", "ыла", "ена", "ейте", "уйте", "ите", "или", "ыли", "ей", "уй", "ил", "ыл", "им", "ым", "ен", "ило", "ыло", "ено", "ят", "ует", "уют", "ит", "ыт", "ены", "ить", "ыть", "ишь", "ую", "ю", "ла", "на", "ете", "йте", "ли", "й", "л", "ем", "н", "ло", "ет", "ют", "ны", "ть", "ешь", "нно"};
        String[] nounEndings = {"а", "ев", "ов", "ье", "иями", "ями", "ами", "еи", "ии", "и", "ией", "ей", "ой", "ий", "й", "иям", "ям", "ием", "ем", "ам", "ом", "о", "у", "ах", "иях", "ях", "ы", "ь", "ию", "ью", "ю", "ия", "ья", "я", "ок", "мва", "яна", "ровать", "ег", "ги", "га", "сть", "сти"};
        String[] adverbEndings = {"чно", "еко", "соко", "боко", "роко", "имо", "мно", "жно", "жко", "ело", "тно", "льно", "здо", "зко", "шо", "хо", "но"};
        String[] numeralEndings = {"чуть", "много", "мало", "еро", "вое", "рое", "еро", "сти", "одной", "двух", "рех", "еми", "яти", "ьми", "ати", "дного", "сто", "ста", "тысяча", "тысячи", "две", "три", "одна", "умя", "тью", "мя", "тью", "мью", "тью", "одним"};
        String[] conjunctionEndings = {"более", "менее", "очень", "крайне", "скоре", "некотор", "кажд", "други", "котор", "когд", "однак", "если", "чтоб", "хот", "смотря", "как", "также", "так", "зато", "что", "или", "потом", "эт", "тог", "тоже", "словно", "ежели", "кабы", "коли", "ничем", "чем"};
        String[] prepositionEndings = {"в", "на", "по", "из"};
        String[] personalPronounEndings = {"я", "ты", "он", "она", "оно", "они", "вы", "меня", "мне", "меня", "мной", "мною", "тебя", "тебе", "тобой", "тобою", "его", "него", "ему", "нему", "его", "им", "ним", "ее", "нее", "ей", "ней", "ею", "нею", "его", "него", "ему", "нему", "им", "ним"};
        String[] pronounEndings = {"кто", "что", "какой", "каков", "чей", "который", "сколько", "этот", "эта", "это", "эти", "тот", "та", "то", "те", "такой", "такая", "такое", "такие", "таков", "такова", "таково", "таковы", "сей", "сия", "сие", "сии", "все", "весь", "всяк", "всякий", "любой", "каждый", "сам", "самый", "другой", "иной", "никто", "ничто", "некого", "нечего", "нисколько", "никакой", "ничей", "некто", "нечто", "некий", "некторый", "несколько"};
        String[] particleEndings = {"то", "либо", "нибудь", "не", "ни", "бы", "же"};

        ENDINGS.put(ADJECTIVE, Arrays.asList(adjectiveEndings));
        ENDINGS.put(COMMUNION, Arrays.asList(communionEndings));
        ENDINGS.put(VERB, Arrays.asList(verbEndings));
        ENDINGS.put(NOUN, Arrays.asList(nounEndings));
        ENDINGS.put(ADVERB, Arrays.asList(adverbEndings));
        ENDINGS.put(NUMERAL, Arrays.asList(numeralEndings));
        ENDINGS.put(CONJUNCTION, Arrays.asList(conjunctionEndings));
        ENDINGS.put(PREPOSITION, Arrays.asList(prepositionEndings));
        ENDINGS.put(PERSONAL_PRONOUN, Arrays.asList(personalPronounEndings));
        ENDINGS.put(PRONOUN, Arrays.asList(pronounEndings));
        ENDINGS.put(PARTICLE, Arrays.asList(particleEndings));
    }

    @Override
    public PartOfSpeech get(String word) {
        Set<PartOfSpeech> supposedPartOfSpeech = new HashSet<>();
        for (PartOfSpeech partOfSpeech : ENDINGS.keySet()) {
            for (String part : ENDINGS.get(partOfSpeech)) {
                switch (partOfSpeech) {
                    case PERSONAL_PRONOUN:
                    case PRONOUN:
                    case PREPOSITION:
                    case PARTICLE:
                        if (word.equals(part)) {
                            supposedPartOfSpeech.add(partOfSpeech);
                        }
                        break;
                    case CONJUNCTION:
                        if (word.startsWith(part)) {
                            supposedPartOfSpeech.add(partOfSpeech);
                        }
                        break;
                    default:
                        if (word.endsWith(part)) {
                            supposedPartOfSpeech.add(partOfSpeech);
                        }
                }
            }
        }

        if (supposedPartOfSpeech.contains(PERSONAL_PRONOUN)) {
            return PERSONAL_PRONOUN;
        } else if (supposedPartOfSpeech.contains(PRONOUN)) {
            return PRONOUN;
        } else if (supposedPartOfSpeech.contains(PREPOSITION)) {
            return PREPOSITION;
        } else if (supposedPartOfSpeech.contains(PARTICLE)) {
            return PARTICLE;
        } else if (supposedPartOfSpeech.contains(CONJUNCTION)) {
            return CONJUNCTION;
        } else if (!supposedPartOfSpeech.isEmpty()) {
            for (PartOfSpeech partOfSpeech : ENDINGS.keySet()) {
                if (supposedPartOfSpeech.contains(partOfSpeech)) {
                    return partOfSpeech;
                }
            }
        }
        return null;
    }
}
