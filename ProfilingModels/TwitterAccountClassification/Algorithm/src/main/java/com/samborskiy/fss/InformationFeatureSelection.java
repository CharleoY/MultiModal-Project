package com.samborskiy.fss;

import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.attributeSelection.InfoGainAttributeEval;
import weka.core.Attribute;
import weka.core.Instances;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

/**
 * Feature selection algorithm uses mutual information like a selection parameter.
 *
 * @author Whiplash
 * @see <a href="https://en.wikipedia.org/wiki/Mutual_information">Mutual information</a>
 */
public class InformationFeatureSelection extends FeatureSelection {

    private final int n;

    public InformationFeatureSelection(int n) {
        this.n = n;
    }

    @Override
    public Instances select(Instances instances) {
        try {
            Instances copiedInstances = new Instances(instances);
            Set<Map.Entry<String, Double>> sortedStatistics = getStatistics(copiedInstances);
            sortedStatistics.stream().filter(entry -> copiedInstances.numAttributes() > n).forEach(entry -> {
                Attribute attribute = copiedInstances.attribute(entry.getKey());
                copiedInstances.deleteAttributeAt(attribute.index());
            });
            return copiedInstances;
        } catch (Exception e) {
            return null;
        }
    }

    /**
     * Returns sorted by mutual information set of attributes.
     *
     * @param instances data which will apply algorithm
     * @return set of attributes
     * @throws Exception if the attribute could not be evaluated
     */
    private Set<Map.Entry<String, Double>> getStatistics(Instances instances) throws Exception {
        InfoGainAttributeEval infoGainAttributeEval = new InfoGainAttributeEval();
        infoGainAttributeEval.buildEvaluator(instances);
        Map<String, Double> iGains = new HashMap<>();
        for (int i = 0; i < instances.numAttributes() - 1; i++) {
            String name = instances.attribute(i).name();
            double iGain = infoGainAttributeEval.evaluateAttribute(i);
            iGains.put(name, iGain);
        }
        return entriesSortedByValues(iGains);
    }

    private <K, V extends Comparable<V>> Set<Map.Entry<K, V>> entriesSortedByValues(Map<K, V> map) {
        Set<Map.Entry<K, V>> sortedEntries = new TreeSet<>(
                (e1, e2) -> {
                    int res = e1.getValue().compareTo(e2.getValue());
                    return res != 0 ? res : 1;
                }
        );
        sortedEntries.addAll(map.entrySet());
        return sortedEntries;
    }

    @Override
    protected ASSearch getSearcher() {
        return null;
    }

    @Override
    protected ASEvaluation getEvaluator() {
        return null;
    }

    @Override
    public String toString() {
        return super.toString() + "(" + n + ")";
    }
}
