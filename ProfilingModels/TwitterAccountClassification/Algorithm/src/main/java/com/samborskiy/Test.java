package com.samborskiy;

import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.core.Instances;

import java.util.Random;

/**
 * Test of classifier to calculate F-measure using k-fold cross-validation and confusion matrix.
 *
 * @author Whiplash
 * @see <a href="https://en.wikipedia.org/wiki/F1_score">F-measure</a>
 * @see <a href="https://en.wikipedia.org/wiki/Cross-validation_(statistics)">Cross-validation</a>
 * @see <a href="https://en.wikipedia.org/wiki/Confusion_matrix">Confusion matrix</a>
 */
class Test {

    private final Classifier classifier;
    private final Instances instances;

    public Test(Classifier classifier, Instances instances) {
        this.instances = instances;
        this.classifier = classifier;
    }

    /**
     * Runs k-folds cross-validation to calculate F-measure of {@code instances}.
     *
     * @param folds number of folds
     * @return F-measure of data
     * @throws Exception if {@link weka.classifiers.Evaluation} cannot be build
     */
    public double crossValidation(int folds) throws Exception {
        Evaluation evaluation = new Evaluation(instances);
        evaluation.crossValidateModel(classifier, instances, folds, new Random(1));
        return getFMeasure(evaluation, instances.numClasses());
    }

    private double getFMeasure(Evaluation evaluation, int classNumber) {
        double precision = 0.;
        double recall = 0.;
        for (int i = 0; i < classNumber; i++) {
            precision += evaluation.precision(i);
            recall += evaluation.recall(i);
        }
        precision /= 3;
        recall /= 3;
        return 2 * precision * recall / (precision + recall);
    }
}
