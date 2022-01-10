package com.samborskiy.fss.selection;

import com.samborskiy.fss.FeatureSelection;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.attributeSelection.ConsistencySubsetEval;
import weka.attributeSelection.ScatterSearchV1;

/**
 * Consistency feature selection algorithm.
 *
 * @author Whiplash
 */
public class Cons_SS extends FeatureSelection {

    @Override
    protected ASSearch getSearcher() {
        return new ScatterSearchV1();
    }

    @Override
    protected ASEvaluation getEvaluator() {
        return new ConsistencySubsetEval();
    }
}
