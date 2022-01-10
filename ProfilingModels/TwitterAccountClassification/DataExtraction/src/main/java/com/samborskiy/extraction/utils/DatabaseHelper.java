package com.samborskiy.extraction.utils;

import com.samborskiy.extraction.entity.Configuration;
import twitter4j.User;

import java.io.File;
import java.sql.*;

/**
 * Class which help user interact with database.
 *
 * @author Whiplash
 */
public class DatabaseHelper implements AutoCloseable {

    /**
     * Name of table column with user's id.
     */
    public static final String USER_ID = "user_id";
    /**
     * Name of table column with user's screen name.
     */
    public static final String SCREEN_NAME = "screen_name";
    /**
     * Name of table column with tweets.
     */
    public static final String TWEETS = "tweets";
    /**
     * Name of table column with user type (0 - personal account, 1 - corporate account).
     */
    public static final String ACCOUNT_TYPE = "account_type";
    public static final String FOLLOWERS = "follower_number";
    public static final String FOLLOWING = "following_number";
    public static final String VERIFIED = "is_verified";
    public static final String FAVOURITE = "favourite_number";
    private static final String DATABASE_URL = "jdbc:sqlite:%s";
    /**
     * Name of table.
     */
    private static final String TABLE_NAME = "twitter_data";
    private static final String CREATE_TABLE = "CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " ("
            + USER_ID + " INTEGER PRIMARY KEY NOT NULL, "
            + SCREEN_NAME + " VARCHAR(40) UNIQUE NOT NULL, "
            + TWEETS + " TEXT, "
            + ACCOUNT_TYPE + " INTEGER NOT NULL, "
            + FOLLOWERS + " INTEGER NOT NULL, "
            + FOLLOWING + " INTEGER NOT NULL, "
            + VERIFIED + " INTEGER NOT NULL, "
            + FAVOURITE + " INTEGER NOT NULL);";
    private static final String INSERT_QUERY = "INSERT INTO " + TABLE_NAME + " VALUES (?, ?, ?, ?, ?, ?, ?, ?);";
    private static final String SELECT_QUERY_USER_ID = "SELECT %s FROM " + TABLE_NAME + " WHERE " + USER_ID + " = %d;";
    private static final String SELECT_QUERY_SCREEN_NAME = "SELECT %s FROM " + TABLE_NAME + " WHERE " + SCREEN_NAME + " = \'%s\';";
    private static final String SELECT_ALL_QUERY = "SELECT * FROM " + TABLE_NAME + ";";
    private static final String DELETE_QUERY_EMPTY_ROW = "DELETE FROM " + TABLE_NAME + " WHERE " + TWEETS + " = '[]';";
    private static final String DELETE_QUERY_SCREEN_NAME = "DELETE FROM " + TABLE_NAME + " WHERE " + SCREEN_NAME + " = '%s';";

    private Configuration configuration;
    private Connection connection;

    /**
     * Creates new instance of {@code DatabaseHelper} with
     * initialize {@code configuration}.
     *
     * @param configuration needed to create new database or connect to existing
     * @throws java.lang.Exception see {@link #connect()}
     */
    public DatabaseHelper(Configuration configuration) throws Exception {
        this.configuration = configuration;
        connect();
    }

    /**
     * Creates a database connection.
     *
     * @throws java.lang.Exception if connection is failed (e.g. bad {@code databasePath} in configuration)
     */
    private void connect() throws Exception {
        Class.forName("org.sqlite.JDBC");
        File databasePath = new File(configuration.getDatabasePath());
        File databaseFolder = getFolder(databasePath);
        if (databaseFolder.exists() || databaseFolder.mkdirs()) {
            String databaseUrl = String.format(DATABASE_URL, configuration.getDatabasePath());
            connection = DriverManager.getConnection(databaseUrl);
        }
    }

    private File getFolder(File file) {
        String absolutePath = file.getAbsolutePath();
        return new File(absolutePath.substring(0, absolutePath.lastIndexOf(File.separator)));
    }

    /**
     * Creates table {@link #TABLE_NAME} if this table not exists.
     *
     * @return {@code true} if table is create
     */
    public boolean createTable() {
        try (Statement statement = connection.createStatement()) {
            return statement.execute(CREATE_TABLE);
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    /**
     * Inserts value into table.
     *
     * @param userId      user's twitter id
     * @param user        user's structure with information
     * @param tweets      user's tweets
     * @param accountType {@code 0} if it personal account else {@code 1}
     * @return {@code true} if insert is complete
     */
    public boolean insert(long userId, User user, String tweets, int accountType) {
        try (PreparedStatement statement = connection.prepareStatement(INSERT_QUERY)) {
            statement.setLong(1, userId);
            statement.setString(2, user.getScreenName());
            statement.setString(3, tweets);
            statement.setInt(4, accountType);
            statement.setInt(5, user.getFollowersCount());
            statement.setInt(6, user.getFriendsCount());
            statement.setInt(7, user.isVerified() ? 1 : 0);
            statement.setInt(8, user.getFavouritesCount());
            statement.executeUpdate();
            return true;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    /**
     * Returns user screen name.
     *
     * @param userId user's twitter id
     * @return user screen name
     */
    public String getScreenName(long userId) {
        try (Statement statement = connection.createStatement()) {
            String selectQuery = String.format(SELECT_QUERY_USER_ID, SCREEN_NAME, userId);
            ResultSet set = statement.executeQuery(selectQuery);
            return set.getString(SCREEN_NAME);
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * Returns user tweets.
     *
     * @param userId user's twitter id
     * @return user tweets
     */
    public String getTweets(long userId) {
        try (Statement statement = connection.createStatement()) {
            String selectQuery = String.format(SELECT_QUERY_USER_ID, TWEETS, userId);
            ResultSet set = statement.executeQuery(selectQuery);
            return set.getString(TWEETS);
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * Returns account type.
     *
     * @param userId user's twitter id
     * @return account type
     */
    public int getAccountType(long userId) {
        try (Statement statement = connection.createStatement()) {
            String selectQuery = String.format(SELECT_QUERY_USER_ID, ACCOUNT_TYPE, userId);
            ResultSet set = statement.executeQuery(selectQuery);
            return set.getInt(ACCOUNT_TYPE);
        } catch (SQLException e) {
            e.printStackTrace();
            return -1;
        }
    }

    /**
     * Returns user tweets.
     *
     * @param screenName screen name of user
     * @return user tweets
     */
    public String getTweets(String screenName) {
        try (Statement statement = connection.createStatement()) {
            String selectQuery = String.format(SELECT_QUERY_SCREEN_NAME, TWEETS, screenName);
            ResultSet set = statement.executeQuery(selectQuery);
            return set.getString(TWEETS);
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * Returns account type.
     *
     * @param screenName screen name of user
     * @return account type
     */
    public int getAccountType(String screenName) {
        try (Statement statement = connection.createStatement()) {
            String selectQuery = String.format(SELECT_QUERY_SCREEN_NAME, ACCOUNT_TYPE, screenName);
            ResultSet set = statement.executeQuery(selectQuery);
            return set.getInt(ACCOUNT_TYPE);
        } catch (SQLException e) {
            e.printStackTrace();
            return -1;
        }
    }

    /**
     * Checks has user with {@code screenName} in database.
     *
     * @param screenName screen name of user
     * @return {@code true} if database contains user with this {@code screenName}, {@code false} otherwise
     */
    public boolean hasUser(String screenName) {
        try (Statement statement = connection.createStatement()) {
            String selectQuery = String.format(SELECT_QUERY_SCREEN_NAME, TWEETS, screenName);
            ResultSet set = statement.executeQuery(selectQuery);
            return !set.isAfterLast();
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    /**
     * Checks has user with {@code screenName} in database.
     *
     * @param userId id of user
     * @return {@code true} if database contains user with this {@code screenName}, {@code false} otherwise
     */
    public boolean hasUser(long userId) {
        try (Statement statement = connection.createStatement()) {
            String selectQuery = String.format(SELECT_QUERY_USER_ID, TWEETS, userId);
            ResultSet set = statement.executeQuery(selectQuery);
            return !set.isAfterLast();
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    /**
     * Removes all row where tweet field is empty (= []).
     */
    public void deleteEmptyTweetsRow() {
        try (Statement statement = connection.createStatement()) {
            statement.execute(DELETE_QUERY_EMPTY_ROW);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    /**
     * Removes row from database by {@code screenName}.
     *
     * @param screenName screen name of user
     */
    public void deleteByScreenName(String screenName) {
        try (Statement statement = connection.createStatement()) {
            String query = String.format(DELETE_QUERY_SCREEN_NAME, screenName);
            statement.execute(query);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    /**
     * Returns {@link java.sql.ResultSet} with all table data.
     * ATTENTION: you must close the cursor yourself (call method close())
     *
     * @return all table data
     */
    public ResultSet getAll() {
        try {
            Statement statement = connection.createStatement();
            return statement.executeQuery(SELECT_ALL_QUERY);
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    @Override
    public void close() throws Exception {
        if (connection != null) {
            connection.close();
        }
    }
}
