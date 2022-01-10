package com.samborskiy.fss.selection;

import com.samborskiy.fss.FeatureSelection;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.attributeSelection.BestFirst;
import weka.attributeSelection.ConsistencySubsetEval;

/**
 * Consistency feature selection algorithm.
 *
 * @author Whiplash
 */
public class Cons_BiS extends FeatureSelection {

    @Override
    protected ASSearch getSearcher() {
        return new BestFirst();
    }

    @Override
    protected String[] getSearcherOptions() {
        return new String[]{"-D", "2"};
    }

    @Override
    protected ASEvaluation getEvaluator() {
        return new ConsistencySubsetEval();
    }
}
