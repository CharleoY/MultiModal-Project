package com.samborskiy.fss.selection;

import com.samborskiy.fss.FeatureSelection;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.attributeSelection.ConsistencySubsetEval;
import weka.attributeSelection.GreedyStepwise;

/**
 * Consistency feature selection algorithm.
 *
 * @author Whiplash
 */
public class Cons_SWS extends FeatureSelection {

    @Override
    protected ASSearch getSearcher() {
        return new GreedyStepwise();
    }

    @Override
    protected ASEvaluation getEvaluator() {
        return new ConsistencySubsetEval();
    }
}
