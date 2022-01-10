package com.samborskiy.attributes.sign;

import com.samborskiy.attributes.AttributeFunction;
import com.samborskiy.entity.sequences.SignSequence;

import java.util.ArrayList;
import java.util.List;

/**
 * Function based on using signs in account.
 *
 * @author Whiplash
 */
public abstract class SignFunction extends AttributeFunction {

    public static final List<SignSequence> SIGNS = new ArrayList<>();

    static {
        SIGNS.add(new SignSequence("stress", "`"));
        SIGNS.add(new SignSequence("tilde", "~"));
        SIGNS.add(new SignSequence("exclamation_point", "!"));
        SIGNS.add(new SignSequence("at", "@"));
        SIGNS.add(new SignSequence("hash", "#"));
        SIGNS.add(new SignSequence("dollar_sign", "$"));
        SIGNS.add(new SignSequence("percent", "%"));
        SIGNS.add(new SignSequence("exponent", "^"));
        SIGNS.add(new SignSequence("ampersand", "&"));
        SIGNS.add(new SignSequence("multiply", "*"));
        SIGNS.add(new SignSequence("opening_parenthesis", "("));
        SIGNS.add(new SignSequence("closing_parenthesis", ")"));
        SIGNS.add(new SignSequence("minus", "-"));
        SIGNS.add(new SignSequence("underline", "_"));
        SIGNS.add(new SignSequence("plus", "+"));
        SIGNS.add(new SignSequence("equals", "="));
        SIGNS.add(new SignSequence("opening_bracket", "["));
        SIGNS.add(new SignSequence("opening_brace", "{"));
        SIGNS.add(new SignSequence("closing_bracket", "]"));
        SIGNS.add(new SignSequence("closing_brace", "}"));
        SIGNS.add(new SignSequence("backslash", "\\"));
        SIGNS.add(new SignSequence("vertical_slash", "|"));
        SIGNS.add(new SignSequence("semicolon", ";"));
        SIGNS.add(new SignSequence("colon", ":"));
        SIGNS.add(new SignSequence("apostrophe", "'"));
        SIGNS.add(new SignSequence("quote", "\""));
        SIGNS.add(new SignSequence("comma", ","));
        SIGNS.add(new SignSequence("less_than", "<"));
        SIGNS.add(new SignSequence("point", "."));
        SIGNS.add(new SignSequence("great_than", ">"));
        SIGNS.add(new SignSequence("divide", "/"));
        SIGNS.add(new SignSequence("question_mark", "?"));
        SIGNS.add(new SignSequence("number_sign", "№"));
    }
}
