package com.samborskiy.extraction.utils;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.io.StringWriter;

/**
 * Class for serialize and deserialize json object.
 *
 * @author Whiplash
 */
public class EntityUtil {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    private EntityUtil() {
    }

    /**
     * Deserializes json object.
     *
     * @param jsonData representation of an object json format
     * @param tClass   class of resulting object
     * @param <T>      type of resulting object
     * @return instance of object
     * @throws IOException if {@code jsonData} has incorrect json object format
     */
    public static <T> T deserialize(byte[] jsonData, Class<T> tClass) throws IOException {
        return MAPPER.readValue(jsonData, tClass);
    }

    /**
     * Serelializes {@code object} to json format string.
     *
     * @param object object which is going to serialize
     * @return resulting string
     */
    public static String serialize(Object object) {
        StringWriter str = new StringWriter();
        try {
            MAPPER.writeValue(str, object);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return str.toString();
    }

}
