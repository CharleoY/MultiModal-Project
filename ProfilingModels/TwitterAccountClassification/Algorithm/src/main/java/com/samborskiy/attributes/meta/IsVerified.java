package com.samborskiy.attributes.meta;

import com.samborskiy.attributes.AttributeFunction;
import com.samborskiy.entity.Account;
import com.samborskiy.entity.Attribute;

import java.util.ArrayList;
import java.util.List;

/**
 * Is account verified or not.
 *
 * @author Whiplash
 */
public class IsVerified extends AttributeFunction {

    @Override
    public String getName() {
        return "is_verified";
    }

    @Override
    public List<Attribute> apply(Account account) {
        List<Attribute> attributes = new ArrayList<>();
        attributes.add(new Attribute(account.getVerified(), getName()));
        return attributes;
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        // empty ...
    }
}
