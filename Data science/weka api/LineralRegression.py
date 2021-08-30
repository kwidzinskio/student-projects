
import weka.core.jvm as jvm
from weka.core.classes import Random
from weka.core.converters import Loader
from weka.core.dataset import Instances
from weka.classifiers import Classifier, Evaluation, PredictionOutput
from weka.filters import Filter
import weka.plot.classifiers as plot_cls

jvm.start()



# load a numeric dataset
print("------------------ Loading dataset ------------------ ")
loader = Loader("weka.core.converters.ArffLoader")
data0 = loader.load_file("C:/diabetes.arff")
tobin = Filter("weka.filters.unsupervised.attribute.NominalToBinary",
  options = ["-R", "9"])
tobin.inputformat(data0)
data11 = tobin.filter(data0)
# data1.class_is_last()

r0 = Filter("weka.filters.unsupervised.attribute.Remove",
  options = ["-R", "3, 4, 5, 7, 8"])
r0.inputformat(data11)
data1 = r0.filter(data11)
data1.class_is_last()

# predicting lineral regression
print("------------------  Predicting LinearRegression on diabetes ------------------ ")
classifier = Classifier(classname="weka.classifiers.functions.LinearRegression", options=["-S", "1", "-C"])
classifier.build_classifier(data1)
print(classifier)
evaluation = Evaluation(data1)
evaluation.crossvalidate_model(classifier, data1, 10, Random(42))
print(evaluation.summary())
plot_cls.plot_classifier_errors(evaluation.predictions, absolute=False, wait=True)

# filters
print("------------------  Adding filters ------------------ ")
addclass = Filter(
    classname="weka.filters.supervised.attribute.AddClassification",
    options=["-classification", "-W", '"weka.classifiers.functions.LinearRegression" -S 0 -R 1.0E-8 -num-decimal-places 4'])
addclass.inputformat(data1)
data2 = addclass.filter(data1)

r = Filter("weka.filters.unsupervised.attribute.Remove",
  options = ["-R", "1-3"])
r.inputformat(data2)
data3 = r.filter(data2)

reord = Filter("weka.filters.unsupervised.attribute.Copy",
  options = ["-R", "1"])
reord.inputformat(data3)
data4 = reord.filter(data3)

r = Filter("weka.filters.unsupervised.attribute.Remove",
  options = ["-R", "1"])
r.inputformat(data4)
data5 = r.filter(data4)
data5.no_class()

tobin = Filter("weka.filters.unsupervised.attribute.NumericToBinary",
  options = ["-R", "2"])
tobin.inputformat(data5)
data6 = tobin.filter(data5)
data6.class_is_last()

# classifier
print("------------------ Applying OneR to randomized data ------------------")
classifier = Classifier(classname="weka.classifiers.rules.OneR", options=["-B", "40"])

# randomize data
folds = 10
seed = 1
rnd = Random(seed)
rand_data = Instances.copy_instances(data6)
rand_data.randomize(rnd)
pred_output = PredictionOutput(
    classname="weka.classifiers.evaluation.output.prediction.PlainText", options=["-distribution", "error"])
evl = Evaluation(rand_data)
for i in range(folds):
    train = rand_data.train_cv(folds, i) # Generates a training fold for cross-validation.
    test = rand_data.test_cv(folds, i) # Generates a test fold for cross-validation.

# build and evaluate classifier
classifier.build_classifier(train)
evl.test_model(classifier, test, output=pred_output)


print("")
print("========== Output =========")
print("Classifier: " + classifier.to_commandline())
print("Dataset: " + data6.relationname)
print("Folds: " + str(10))
print("Seed: " + str(1))
print("")
print(classifier)
print(evl.summary("=== OneR on diabetes (stats) ===", False))
print(evl.class_details())
print(evl.matrix("=== OneR on diabetes (confusion matrix) ==="))
print(pred_output)
print("areaUnderPRC/0: " + str(evl.area_under_prc(0)))
print("weightedAreaUnderPRC: " + str(evl.weighted_area_under_prc))
print("areaUnderROC/1: " + str(evl.area_under_roc(1)))
print("weightedAreaUnderROC: " + str(evl.weighted_area_under_roc))
print("avgCost: " + str(evl.avg_cost))
print("totalCost: " + str(evl.total_cost))
print("falseNegativeRate: " + str(evl.false_negative_rate(1)))
print("weightedFalseNegativeRate: " + str(evl.weighted_false_negative_rate))
print("numFalseNegatives: " + str(evl.num_false_negatives(1)))
print("trueNegativeRate: " + str(evl.true_negative_rate(1)))
print("weightedTrueNegativeRate: " + str(evl.weighted_true_negative_rate))
print("numTrueNegatives: " + str(evl.num_true_negatives(1)))
print("falsePositiveRate: " + str(evl.false_positive_rate(1)))
print("weightedFalsePositiveRate: " + str(evl.weighted_false_positive_rate))
print("numFalsePositives: " + str(evl.num_false_positives(1)))
print("truePositiveRate: " + str(evl.true_positive_rate(1)))
print("weightedTruePositiveRate: " + str(evl.weighted_true_positive_rate))
print("numTruePositives: " + str(evl.num_true_positives(1)))


jvm.stop()