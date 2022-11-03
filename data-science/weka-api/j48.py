
import weka.core.jvm as jvm
from weka.core.classes import Random
from weka.core.converters import Loader
from weka.core.dataset import Instances
from weka.classifiers import Classifier, Evaluation, PredictionOutput
import weka.plot.classifiers as plot_cls
import weka.plot.dataset as pld

jvm.start()


# load a dataset
print("------------------ Loading dataset ------------------ ")
data_file = "C:/diabetes.arff"
loader = Loader("weka.core.converters.ArffLoader")
data = loader.load_file(data_file)
data.class_is_last()

# classifier
print("------------------ Applying J48 to randomized data ------------------")
classifier = Classifier(classname="weka.classifiers.trees.J48", options=["-C", "0.25", "-M", "10"])

# randomize data
folds = 10
seed = 1
rnd = Random(seed)
rand_data = Instances.copy_instances(data)
rand_data.randomize(rnd)
pred_output = PredictionOutput(
    classname="weka.classifiers.evaluation.output.prediction.PlainText", options=["-distribution"])
evaluation = Evaluation(rand_data)
for i in range(folds):
    train = rand_data.train_cv(folds, i) # Generates a training fold for cross-validation.
    test = rand_data.test_cv(folds, i) # Generates a test fold for cross-validation.

# build and evaluate classifier
classifier.build_classifier(train)
evaluation.test_model(classifier, test, output=pred_output)

print("")
print("========= Output =========")
print("Classifier: " + classifier.to_commandline())
print("Dataset: " + data.relationname)
print("Folds: " + str(10))
print("Seed: " + str(1))
print("")
print("")
print(classifier)
print(evaluation.summary())
print(evaluation.class_details())
print(evaluation.matrix())
print(pred_output)
print("areaUnderPRC/0: " + str(evaluation.area_under_prc(0)))
print("weightedAreaUnderPRC: " + str(evaluation.weighted_area_under_prc))
print("areaUnderROC/1: " + str(evaluation.area_under_roc(1)))
print("weightedAreaUnderROC: " + str(evaluation.weighted_area_under_roc))
print("avgCost: " + str(evaluation.avg_cost))
print("totalCost: " + str(evaluation.total_cost))
print("falseNegativeRate: " + str(evaluation.false_negative_rate(1)))
print("weightedFalseNegativeRate: " + str(evaluation.weighted_false_negative_rate))
print("numFalseNegatives: " + str(evaluation.num_false_negatives(1)))
print("trueNegativeRate: " + str(evaluation.true_negative_rate(1)))
print("weightedTrueNegativeRate: " + str(evaluation.weighted_true_negative_rate))
print("numTrueNegatives: " + str(evaluation.num_true_negatives(1)))
print("falsePositiveRate: " + str(evaluation.false_positive_rate(1)))
print("weightedFalsePositiveRate: " + str(evaluation.weighted_false_positive_rate))
print("numFalsePositives: " + str(evaluation.num_false_positives(1)))
print("truePositiveRate: " + str(evaluation.true_positive_rate(1)))
print("weightedTruePositiveRate: " + str(evaluation.weighted_true_positive_rate))
print("numTruePositives: " + str(evaluation.num_true_positives(1)))
plot_cls.plot_roc(
    evaluation, title="ROC diabetes",
    class_index=range(0, test.class_attribute.num_values), wait=False)
plot_cls.plot_prc(
    evaluation, title="PRC diabetes",
    class_index=range(0, test.class_attribute.num_values), wait=False)
for i in range(1,9):
    for j in range (i,9):
        pld.scatter_plot(data, i, j, percent=100)



jvm.stop()

