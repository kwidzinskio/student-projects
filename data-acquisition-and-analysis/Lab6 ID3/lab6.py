import pandas as pd
import numpy as np
import json

def calculate_entropy(dataset, label, classes):
    total_entropy = 0
    dataset_size = len(dataset.index)
    for label_class in classes:
        class_count = dataset[label].value_counts()[label_class]
        class_probability = class_count / dataset_size
        class_entropy = - class_probability * np.log2(class_probability)
        total_entropy += class_entropy
    return total_entropy

def calculate_information_gain(dataset, label, classes, feature):
    feature_information = 0
    feature_values = dataset[feature].unique()
    dataset_size = len(dataset.index)
    for feature_value in feature_values:
        feature_entropy = 0
        feature_size = dataset[feature].value_counts()[feature_value]
        for feature_label_class in classes:
            feature_label_class_count = dataset[(dataset[label] == feature_label_class) & (dataset[feature] == feature_value)].shape[0]
            if feature_label_class_count != 0:
                feature_class_probability = feature_label_class_count / feature_size
                feature_value_entropy = - feature_class_probability * np.log2(feature_class_probability)
                feature_entropy += feature_value_entropy
        feature_value_probability = feature_size / dataset_size
        feature_value_info_gain = feature_value_probability * feature_entropy
        feature_information += feature_value_info_gain
    information_gain = calculate_entropy(dataset, label, classes) - feature_information
    return information_gain

def find_next_node(dataset, label, classes):
    features_info_dict = {}
    feature_names = list(dataset.columns.drop(label))
    for feature in feature_names:
        feature_info_gain = calculate_information_gain(dataset, label, classes, feature)
        features_info_dict[feature] = feature_info_gain
    max_info_feature = max(features_info_dict, key=features_info_dict.get)
    return max_info_feature

def generate_sub_tree(dataset, label, feature):
    tree = {}
    feature_values = dataset[feature].unique()
    for feature_value in feature_values:
        feature_label_values = dataset[dataset[feature] == feature_value]
        has_unique_label = feature_label_values[label].eq(feature_label_values[label].iloc[0]).all()
        if has_unique_label:
             feature_label_class = feature_label_values.iloc[0, feature_label_values.columns.get_loc(label)]
             tree[feature_value] = feature_label_class
        else:
             tree[feature_value] = 'Unknown'
    return tree

def make_tree(dataset, label, classes, old_tree, feature=None):
    if not dataset.empty:
        max_info_feature = find_next_node(dataset, label, classes)
        tree = generate_sub_tree(dataset, label, max_info_feature)
        if not bool(old_tree):
            old_tree[max_info_feature] = tree
            next_tree = old_tree[max_info_feature]
        else:
            old_tree[feature] = {}
            old_tree[feature][max_info_feature] = tree
            next_tree = old_tree[feature][max_info_feature]
        for node, branch in next_tree.items():
            if branch == 'Unknown':
                feature_value_dataset = dataset[dataset[max_info_feature] == node]
                make_tree(feature_value_dataset, label, classes, next_tree, node)

def id3(dataset, label, classes):
    tree = {}
    make_tree(dataset, label, classes, tree)
    return tree

if __name__ == "__main__":
    dataset = pd.read_csv("lab6.csv")
    label = "Choice"
    classes = dataset[label].unique()
    tree = {}
    id3_schema = id3(dataset, label, classes)

    print(json.dumps(id3_schema, sort_keys=True, indent=4))