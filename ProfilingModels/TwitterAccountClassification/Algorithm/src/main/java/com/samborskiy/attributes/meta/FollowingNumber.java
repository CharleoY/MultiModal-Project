package com.samborskiy.attributes.meta;

import com.samborskiy.attributes.AttributeFunction;
import com.samborskiy.entity.Account;
import com.samborskiy.entity.Attribute;

import java.util.ArrayList;
import java.util.List;

/**
 * Number of following in account.
 *
 * @author Whiplash
 */
public class FollowingNumber extends AttributeFunction {

    @Override
    public String getName() {
        return "following_number";
    }

    @Override
    public List<Attribute> apply(Account account) {
        List<Attribute> attributes = new ArrayList<>();
        attributes.add(new Attribute(account.getFollowing(), getName()));
        return attributes;
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        // empty ...
    }
}
