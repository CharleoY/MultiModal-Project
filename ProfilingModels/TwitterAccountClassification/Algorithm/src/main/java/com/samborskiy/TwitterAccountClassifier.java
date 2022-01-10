package com.samborskiy;

import com.samborskiy.attributes.AttributeFunction;
import com.samborskiy.attributes.partofspeech.PartOfSpeechFunction;
import com.samborskiy.attributes.partofspeech.PartOfSpeechPerAccount;
import com.samborskiy.attributes.partofspeech.ParticlePerAccount;
import com.samborskiy.attributes.partofspeech.TweetsWithPartOfSpeech;
import com.samborskiy.attributes.sign.*;
import com.samborskiy.attributes.smile.*;
import com.samborskiy.entity.Account;
import com.samborskiy.entity.ClassifierProperty;
import com.samborskiy.entity.Log;
import com.samborskiy.fss.FeatureSelection;
import com.samborskiy.fss.InformationFeatureSelection;
import com.samborskiy.fss.NoFeatureSelection;
import org.reflections.Reflections;
import weka.classifiers.AbstractClassifier;
import weka.classifiers.Classifier;
import weka.classifiers.trees.RandomForest;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.OptionHandler;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Classifier to identify Twitter account to one of the next types: personal, corporate, character.
 * <br>
 * Defaults use {@link weka.classifiers.trees.RandomForest} classifier as the most effective
 * classifier for solving this problem.
 *
 * @author Whiplash
 */
public class TwitterAccountClassifier {

    private Classifier classifier = new RandomForest();

    {
        try {
            ((OptionHandler) classifier).setOptions(new String[]{"-I", "104"});
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private Instances instances;
    private String relationName;

    /**
     * Creates instance of {@link com.samborskiy.TwitterAccountClassifier classifier} using
     * exist in project folder arff file with name {@code relationName}.
     *
     * @param relationName name of relation
     * @throws IOException if {@code relationName}.arff doesn't exist
     */
    public TwitterAccountClassifier(String relationName) throws IOException {
        this.relationName = relationName;
        initializeInstances();
    }

    /**
     * Creates instance of {@link com.samborskiy.TwitterAccountClassifier classifier} converting
     * {@code accounts} to arff file (into project folder).
     *
     * @param accounts     data which will be converted to arff file
     * @param relationName name of relation
     * @throws IOException if {@code relationName}.arff doesn't exist
     */
    public TwitterAccountClassifier(List<Account> accounts, String relationName) throws ReflectiveOperationException, IOException {
        this.relationName = relationName;
        setAttributes(accounts);
        AccountsToArff.write(accounts.stream()
                .map(Account::getClassId)
                .collect(Collectors.toSet()), accounts, relationName);
        initializeInstances();
    }

    private void initializeInstances() throws IOException {
        try (BufferedReader dataFile = new BufferedReader(new FileReader(relationName + ".arff"))) {
            instances = new Instances(dataFile);
            instances.setClassIndex(instances.numAttributes() - 1);
        }
    }

    /**
     * Builds classifier.
     *
     * @throws Exception if the classifier has not been generated successfully
     */
    public void build() throws Exception {
        classifier.buildClassifier(instances);
    }

    /**
     * Applies feature selection algorithm to {@code instances}.
     *
     * @param featureSelection algorithm which will be used
     */
    public void applyFeatureSelection(FeatureSelection featureSelection) {
        instances = featureSelection.select(instances);
    }

    /**
     * Finds the best feature subset selection algorithm using
     * the F-measure as a parameter for comparison.
     *
     * @param folds folds number (need to k-folds cross-validation)
     * @return the best of feature subset selection algorithm to current data and classifier
     * @throws Exception if test cannot be run
     */
    public FeatureSelection findFeatureSubsetSelectionAlgorithm(int folds) throws Exception {
        List<FeatureSelection> algorithms = getFeaturesSelectionAlgorithms();
        Classifier[] copiedClassifiers = AbstractClassifier.makeCopies(classifier, algorithms.size());
        FeatureSelection maxFSS = null;
        double maxFMeasure = 0.;
        for (int i = 0; i < copiedClassifiers.length; i++) {
            Log.d("Start " + algorithms.get(i).toString());
            double fMeasure = new Test(copiedClassifiers[i], algorithms.get(i).select(instances)).crossValidation(folds);
            Log.d("End with F-measure: " + fMeasure);
            if (fMeasure > maxFMeasure) {
                maxFMeasure = fMeasure;
                maxFSS = algorithms.get(i);
            }
        }
        return maxFSS;
    }

    /**
     * Returns class id of {@code account} (runs {@link #build()} before).
     *
     * @param account account has to be classified
     * @return class id of {@code account}
     * @throws Exception if an error occurred during the prediction
     */
    public int getClassId(Account account) throws Exception {
        setAttributes(account, getAttributeFunctions());
        ArrayList<weka.core.Attribute> attrs = new ArrayList<>();
        for (int i = 0; i < instances.numAttributes(); i++) {
            attrs.add(instances.attribute(i));
        }
        Instances temp = new Instances("temp", attrs, 1);
        temp.setClass(instances.classAttribute());
        temp.add(account.toInstance(attrs));
        return (int) classifier.classifyInstance(temp.get(0));
    }

    /**
     * Returns class id of {@code instance} (runs {@link #build()} before).
     *
     * @param instance account has to be classified (converts to {@link weka.core.Instance})
     * @return class id of {@code instance}
     * @throws Exception if an error occurred during the prediction
     */
    public int getClassId(Instance instance) throws Exception {
        return (int) classifier.classifyInstance(instance);
    }

    private void setAttributes(List<Account> accounts) throws ReflectiveOperationException {
        List<AttributeFunction> functions = getAttributeFunctions();
        for (Account account : accounts) {
            setAttributes(account, functions);
        }
    }

    private void setAttributes(Account account, List<AttributeFunction> functions) {
        for (AttributeFunction function : functions) {
            account.addAll(function.apply(account));
        }
    }

    private List<AttributeFunction> getAttributeFunctions() throws ReflectiveOperationException {
        List<AttributeFunction> accountFunctions = new ArrayList<>();
        // ------- get all attributes function from com.samborskiy.attributes package
        accountFunctions.addAll(getTweetAttributes("com.samborskiy.attributes.length"));
        accountFunctions.addAll(getTweetAttributes("com.samborskiy.attributes.grammar"));
        accountFunctions.addAll(getTweetAttributes("com.samborskiy.attributes.vocabulary"));
        accountFunctions.addAll(getTweetAttributes("com.samborskiy.attributes.hashtag"));
        accountFunctions.addAll(getTweetAttributes("com.samborskiy.attributes.reference"));
        accountFunctions.addAll(getTweetAttributes("com.samborskiy.attributes.personal"));
        accountFunctions.addAll(getTweetAttributes("com.samborskiy.attributes.frequency"));
        accountFunctions.addAll(getTweetAttributes("com.samborskiy.attributes.link"));
        accountFunctions.addAll(getTweetAttributes("com.samborskiy.attributes.meta"));
        accountFunctions.add(new ParticlePerAccount());
        accountFunctions.addAll(PartOfSpeechFunction.SEQUENCES.stream().map(PartOfSpeechPerAccount::new).collect(Collectors.toList()));
        accountFunctions.addAll(PartOfSpeechFunction.SEQUENCES.stream().map(TweetsWithPartOfSpeech::new).collect(Collectors.toList()));
        accountFunctions.add(new AvrSignsNumber());
        accountFunctions.add(new SignLatitude());
        accountFunctions.add(new SignsPerAccount());
        accountFunctions.add(new TweetsWithSigns());
        accountFunctions.addAll(SignFunction.SIGNS.stream().map(SignPerAccount::new).collect(Collectors.toList()));
        accountFunctions.addAll(SignFunction.SIGNS.stream().map(TweetsWithSign::new).collect(Collectors.toList()));
        accountFunctions.add(new DifferentSmiles());
        accountFunctions.add(new TweetsWithSmiles());
        accountFunctions.addAll(SmileFunction.SMILES.stream().map(SmilePerAccount::new).collect(Collectors.toList()));
        accountFunctions.addAll(SmileFunction.SMILES.stream().map(TweetsWithSmile::new).collect(Collectors.toList()));
        // ------- filter attributes by removing extra (using properties of project)
        if (ClassifierProperty.getAttributes() != null) {
            accountFunctions.removeIf(attribute -> !ClassifierProperty.getAttributes().contains(attribute.getName()));
        }
        // -------
        return accountFunctions;
    }

    private List<AttributeFunction> getTweetAttributes(String packageName) throws ReflectiveOperationException {
        return getClasses(packageName, AttributeFunction.class);
    }

    private List<FeatureSelection> getFeaturesSelectionAlgorithms() throws ReflectiveOperationException {
        List<FeatureSelection> featureSelections = new ArrayList<>();
        featureSelections.add(new NoFeatureSelection());
        featureSelections.addAll(getFeaturesSelectionAlgorithms("com.samborskiy.fss.selection"));
        featureSelections.addAll(getFeaturesSelectionAlgorithms("com.samborskiy.fss.extraction"));
        for (int i = 0; i < instances.numAttributes(); i++) {
            featureSelections.add(new InformationFeatureSelection(i));
        }
        return featureSelections;
    }

    private List<FeatureSelection> getFeaturesSelectionAlgorithms(String packageName) throws ReflectiveOperationException {
        return getClasses(packageName, FeatureSelection.class);
    }

    private <E> List<E> getClasses(String packageName, Class<E> type) throws ReflectiveOperationException {
        Reflections reflections = new Reflections(packageName);
        Set<Class<? extends E>> allClasses = reflections.getSubTypesOf(type);
        List<E> classes = new ArrayList<>();
        for (Class clazz : allClasses) {
            if (!Modifier.isAbstract(clazz.getModifiers())) {
                classes.add((E) clazz.newInstance());
            }
        }
        return classes;
    }

    /**
     * Sets new classifier.
     *
     * @param classifier new classifier
     */
    public void setClassifier(Classifier classifier) {
        this.classifier = classifier;
    }
}
