package com.samborskiy.entity;

/**
 * Structure for holding information about attribute (name and value).
 */
public class Attribute {

    private final double value;
    private final String name;

    public Attribute(double value, String name) {
        this.value = value;
        this.name = name;
    }

    public Attribute(double value, Class clazz) {
        this(value, clazz.getSimpleName());
    }

    @Override
    public String toString() {
        return String.format("@attribute %s numeric", name);
    }

    public String getName() {
        return name;
    }

    public double getValue() {
        return value;
    }
}
