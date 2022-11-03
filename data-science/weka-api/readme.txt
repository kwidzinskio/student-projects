Waikato Environment for Knowledge Analysis (WEKA for short) is free software for data mining. The software is a 
comprehensive set of data pre-processing and modeling techniques in the 'drag and drop' system, as well as a tool
for algorithm visualization, data analysis and predictive modeling. For its operation, WEKA uses the Java virtual 
machine - the language in which the WEKA tool was created.

The aim of the project is to present its complex data mining tools. Contrary to what was presented in the theoretical 
part, in the practical part, the use of algorithms was implemented through a script. This approach to the tool enables 
multiple use of a given algorithm by writing the code once, which can be used in multiple implementations. Another 
advantage is that it is easy to create different script variants to test a given theory. In addition, script writing 
is of great educational value - it captures all the steps of 'data mining' from pre-processing, through modeling, 
to algorithm evaluation.

The project uses two algorithms for the classification of the selected data set: through linear regression and the tree 
algorithm. The implementation, initial data processing and model evaluation were performed with the help of the built-in 
version 3.9.5. WEKA software.

The project used a dataset on diabetes incidence - diabetes.arff.

The target variable investigated is whether the patient shows symptoms of diabetes (binary variable). Each instance of 
the data set also contains eight descriptive variables (marked with numbers 1-8 in Fig. 1a.). The entire collection 
contains a total of 768 instances.

The 'python-weka-wrapper' library was used to connect to the Java virtual machine. The next stages of the script 
implementation are loading the data and then creating the classifier. In the case of the tree algorithm, 
'weka.classifiers.trees.J48' was selected, and in the case of linear regression 'weka.classifiers.functions.LinearRegression'. 
The implementation of the J48 algorithm was preceded by the randomization of data by cross-validation, to then evaluate it 
and write the model results.
In the case of linear regression classification, the pre-processing process was more complicated. The data was subjected 
to many filters, the most important of which was the creation of a new attribute in the form of linear regression applied 
to each instance ('weka.filters.supervised.attribute.AddClassification'). Subsequently, unnecessary descriptive variables 
were removed and the target variable was converted to binary form. As a result, a two-dimensional table of records was 
obtained with two variables - a descriptive variable taken from the linear regression analysis, and a target variable in the 
form of {0, 1}, where 1 - means a positive result, and 0 - a negative result. The data processed in this way was subjected to 
the same processes as in the case of the J48 algorithm, except that the classifier for the new data set was the OneR algorithm 
('weka.classifiers.rules.OneR').

The following techniques were used to improve the model:
• the minimum number of objects in the J48 tree leaf was set to 10, from the default value equal to 2. This was achieved by 
adding the value '-M 10' to the classifier. Thanks to this modification, the phenomenon of overfiting is counteracted, and 
the ratio of correctly classified records has increased,
• the attributes that did not significantly affect the linear correlation coefficient in the classification by linear regression 
were removed. The baseline value is a score of 0.5322 for the model assuming the presence of all eight descriptive variables. 
After removing five of them and leaving only 'preg', 'plas' and 'mass', the value of the correlation coefficient remained at the 
level of 0.53.

In the assumed approach to the presentation of the WEKA tool, reliable and satisfactory results of the prediction compliance with 
the target variables were obtained for both classifiers. Both algorithms have a short implementation period and a low load factor.
WEKA is an appropriate tool for data pre-processing, data visualization and evaluation of applied models. It can be successfully 
used in implementations for academic considerations, as it allows you to understand the operation of many data mining algorithms. 
Ease of handling filters, visualizations and model evaluation is particularly important. WEKA owes its universality to its high 
intuitiveness in operation and a wide range of built-in models: classification, machine learning or grouping. Can be easily scaled 
up for commercial use. An interesting approach to the use of WEKI is to use it as a set of libraries called in a specific programming 
language in the form of a script. The above project uses Python as a basic data mining tool and there were no performance differences 
compared to basic Python libraries such as 'scikit learn'.


