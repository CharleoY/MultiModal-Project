package com.samborskiy.fss;

import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.core.Instances;
import weka.core.OptionHandler;
import weka.filters.Filter;
import weka.filters.supervised.attribute.AttributeSelection;

/**
 * Feature subset selection algorithm which reduces the dimension of the feature space.
 *
 * @author Whiplash
 */
public abstract class FeatureSelection {

    /**
     * Reduces the dimension of the feature space.
     *
     * @param instances data which will apply algorithm
     * @return data processed by the algorithm
     */
    public Instances select(Instances instances) {
        try {
            AttributeSelection filter = new AttributeSelection();
            ASSearch searcher = getSearcher();
            ASEvaluation evaluation = getEvaluator();
            if (searcher != null && evaluation != null) {
                if (searcher instanceof OptionHandler) {
                    ((OptionHandler) searcher).setOptions(getSearcherOptions());
                }
                if (evaluation instanceof OptionHandler) {
                    ((OptionHandler) evaluation).setOptions(getEvaluatorOptions());
                }
                filter.setSearch(searcher);
                filter.setEvaluator(evaluation);
                filter.setInputFormat(instances);
                return Filter.useFilter(instances, filter);
            } else {
                return instances;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * Returns searcher of algorithm.
     *
     * @return searcher of algorithm
     */
    protected abstract ASSearch getSearcher();

    /**
     * Returns searcher options (if it implemented {@link weka.core.OptionHandler})
     *
     * @return searcher options
     */
    protected String[] getSearcherOptions() {
        return new String[]{};
    }

    /**
     * Returns evaluator of algorithm.
     *
     * @return evaluator of algorithm
     */
    protected abstract ASEvaluation getEvaluator();

    /**
     * Returns evaluator options (if it implemented {@link weka.core.OptionHandler})
     *
     * @return evaluator options
     */
    protected String[] getEvaluatorOptions() {
        return new String[]{};
    }

    @Override
    public String toString() {
        return getClass().getSimpleName();
    }
}
