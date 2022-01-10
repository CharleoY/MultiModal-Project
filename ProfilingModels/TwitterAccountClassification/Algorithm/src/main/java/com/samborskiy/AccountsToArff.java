package com.samborskiy;

import com.samborskiy.entity.Account;
import com.samborskiy.entity.Attribute;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Collection;
import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;

/**
 * Util to generates arff file using list of {@link com.samborskiy.entity.Account accounts}.
 *
 * @author Whiplash
 */
class AccountsToArff {

    private AccountsToArff() {
    }

    /**
     * Generates arff file from list of accounts.
     *
     * @param types        types of accounts (eg. {0 1 2})
     * @param accounts     data which will be written into file
     * @param relationName name of relation (also future file name)
     * @throws FileNotFoundException if file cannot be created
     */
    public static void write(Collection<Integer> types, List<Account> accounts, String relationName) throws FileNotFoundException {
        if (accounts == null || accounts.isEmpty()) {
            throw new IllegalArgumentException("data can't be null or empty");
        }
        try (PrintWriter writer = new PrintWriter(relationName + ".arff")) {
            printHeader(relationName, writer);
            printArgs(types, accounts, writer);
            printData(accounts, writer);
        }
    }

    private static void printData(List<Account> accounts, PrintWriter writer) {
        writer.println("@data");
        for (Account account : accounts) {
            for (Attribute attribute : account) {
                writer.format(Locale.US, "%f, ", attribute.getValue());
            }
            writer.println(account.getClassId());
        }
    }

    private static void printArgs(Collection<Integer> types, List<Account> accounts, PrintWriter writer) {
        Account account = accounts.get(0);
        account.forEach(writer::println);
        writer.format("@attribute class %s\n",
                types.stream().map(String::valueOf)
                        .collect(Collectors.joining(" ", "{", "}")));
        writer.println();
    }

    private static void printHeader(String relationshipName, PrintWriter writer) {
        writer.format("@relation %s\n", relationshipName);
        writer.println();
    }
}
