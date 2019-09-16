## Purpose:

This project serves to investigate a form of Affinity Analysis known as Market Basket Analysis. 

### Goal:

Given a set of Transactiona data, we seek to find non-obvious relations between sets of items that frequently show up in the transactions. These relationships should be quantified in such as way as to be ranked (some better than others, relative to metrics). We should also be able to display a graph of relationships, as a visual aide. For example, after running the code in the following notebooks, you can generate rule cluster graphs as seen below:

![cluster][rulegraph]


### Libraries Used:

The [mlxtend][mlx] and [pyvis][pyv], pandas and Altair.

### Dataset Used:

For our code experiments, the UCI Online Retail Dataset is utilized. For more details, see [here][uci]

### Presentation and Order of Notebooks:


1) **RetailStoreDataAnalysis:** Does basic EDA and Summaries on the dataset (trend plotting, top products, etc). 

2) **AffinityAnalysis_LearningAssociationRules:** The main notebook. All theory and code experiments are kept in this book. This goes into a lot of detail investigating and understanding the different metrics used to rank and qualify potential rules.

3) **MBA_Usage&Tutorial:** The results from the AffinityAnalysis notebook are summarized and the code refined. Steps to find and refine rules are given. A basic example from Raw Data to a properly refined graphical representation of the rules is given.


### Using the Code Yourself:

Clone this repository, and run the basic example in MBA_Usage&Tutorial to get started. Copy the code into a module.py to use in your own projects.


### References:

1) Ning-Tan, Pan et. al (2012), Chapter 5 - Introduction to Data Mining 2nd Edition, Pearson Education.

2) Azevedo, Paulo J., Jorge Alipio M., (20??) Comparing Rule Measures for Predictive Association Rules, Universitiy of Porto, Portugal

3) Moffitt, Chris (2017): Introduction to Market Basket Analysis in Python, Practical Business Python Blog, url:(https://pbpython.com/market-basket-analysis.html)



[mlx]:http://rasbt.github.io/mlxtend/
[pyv]:https://pyvis.readthedocs.io/en/latest/
[uci]:https://archive.ics.uci.edu/ml/datasets/online+retail
[rulegraph]:/web/img/rule_graph.png