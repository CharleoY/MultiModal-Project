package com.samborskiy.fss.extraction;

import com.samborskiy.fss.FeatureSelection;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.attributeSelection.PrincipalComponents;
import weka.attributeSelection.Ranker;

/**
 * Feature extraction algorithm.
 *
 * @author Whiplash
 * @see <a href="https://en.wikipedia.org/wiki/Principal_component_analysis">PCA</a>
 */
public class PCA extends FeatureSelection {

    @Override
    protected ASSearch getSearcher() {
        return new Ranker();
    }

    @Override
    protected ASEvaluation getEvaluator() {
        return new PrincipalComponents();
    }
}
