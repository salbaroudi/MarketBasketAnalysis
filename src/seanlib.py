
#Makes imports and function calls easier.
#Imports and Settings:
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
from datetime import timedelta
import pyvis


#Settings
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
alt.renderers.enable('notebook')
alt.data_transformers.enable('default', max_rows=None)
#%matplotlib inline 
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 40)
pd.set_option('display.width', 1000)


#support functions:

#Signature: DataFrame, String -> DataFrame
#Purpose: Analyse a given numerical series. Construct a pseudo dataframe that mimics Q1,Q2,Q3 from series.
#add additional outlier/point information for Altair to interpret (in the prod_chart) method.
#Note: I assume 1.5*IRQ for the whiskers.
def df_gen(data,colname):
    df = data[colname]
    qDict = {"min":df.min(),
             "q0":0,
             "q1":df.quantile(0.25),
             "q2":df.median(),
             "q3":df.quantile(0.75),
             "q4":0,
             "max":df.max()}
    qDict["q0"] = qDict["q2"] - 1.5*(qDict["q3"] - qDict["q1"])
    qDict["q4"] = qDict["q2"] + 1.5*(qDict["q3"] - qDict["q1"])

    pseudoDF = pd.DataFrame({colname:colname,"datum":[qDict["q0"],qDict["q1"],qDict["q2"],qDict["q3"],qDict["q4"]]})

    if (qDict["min"] < qDict["q0"]): #Draw a Red Line just outside of Q0
         pseudoDF["outlierL"] = qDict["q0"]
    else:
        pseudoDF["min"] = qDict["min"]

    if (qDict["max"] > qDict["q4"]): #Draw a Red Line just outside of Q4
        pseudoDF["outlierR"] = qDict["q4"]
    else: #Draw a blue line for the maximum
        pseudoDF["max"] = qDict["max"]

    return pseudoDF

#Signature: String -> Boolean
#Check to see if a col type is in the given list.
def checklist(x):
    return (x in ["float32","float64","int16","int32","int64"]) #** Reasonable types? Corner Cases? 

def prod_chart(pseudoDF,colname):
    #Dataframe finished, make our chart.
    chart = alt.Chart(pseudoDF)

    #determine domain:
    axisRange = (pseudoDF["datum"].iloc[4]- pseudoDF["datum"].iloc[0])
    lower = pseudoDF["datum"].iloc[0] - axisRange*0.1
    upper = pseudoDF["datum"].iloc[4] + axisRange*0.1

    #make main chart
    mainChart = chart.mark_boxplot(extent=1.5,size=35,clip=True).encode(
        y=alt.Y(colname+":O",axis=alt.Axis(title=" ")),
        x=alt.X('datum:Q',
                scale=alt.Scale(domain=(lower, upper),zero=False),
                axis=alt.Axis(title=" "))).properties(
        height=100, width=400)

    #now lets determine the layers

    lowerLine = 0
    upperLine = 0

    if "outlierL" in pseudoDF.columns:
        lowerLine = chart.mark_rule(color='red').encode(
        x='outlierL:Q',
        size=alt.value(3))    
    if "min" in pseudoDF.columns:
        lowerLine = chart.mark_rule(color='blue').encode(
        x='min:Q',
        size=alt.value(3))

    if "outlierR" in pseudoDF.columns:
        upperLine = chart.mark_rule(color='red').encode(
        x='outlierR:Q',
        size=alt.value(3))
    if "max" in pseudoDF.columns:
        upperLine = chart.mark_rule(color='blue').encode(
        x='max:Q',
        size=alt.value(3))
        
    return (mainChart + lowerLine + upperLine)    

#Signature: DataFrame -> Chart
#Purpose: Extract all numerical columns form a data frame, and make a stacked bar chart for quick comparison
#of data rangers, outliers, bounds etc. This is a visual representation of the describe() method.

def boxplotblast(df):
    #first, identify numerical columns of dataframe
    dTypeSer = df.dtypes
    hold = dTypeSer.apply(checklist) #Ret bool selector
    numCols = df.columns[hold] #return index object; like an array/list
    finalChart = prod_chart(df_gen(df, numCols[0]),numCols[0]) #limit it for now!

    for i,item in enumerate(numCols[1:]):
        currChart = prod_chart(df_gen(df, item), item)
        finalChart = finalChart & currChart
    
    print("Guide: Blue lines indicate max/min value. Red Lines indicate cutoff of outliers.")
    
    return finalChart


def loadcleandata(cty):
    df = pd.read_excel('./data/online_retail.xlsx') #Why did a 20MB file take 1min to load??
    df['Description'] = df['Description'].str.strip()
    df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
    df['InvoiceNo'] = df['InvoiceNo'].astype('str')
    df = df[~df['InvoiceNo'].str.contains('C')]    
    
    basket = (df[df['Country'] ==cty].groupby(['InvoiceNo', 'Description'])["Quantity"])
    basket = basket.sum().unstack().reset_index().fillna(0).set_index('InvoiceNo') 
    basket_sets = basket.applymap(encode_units) 
    basket_sets.drop('POSTAGE', inplace=True, axis=1)
    return basket_sets

    
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

#Note, you still need to sort the DF of rules that you get.

def getrules(bsets,minsup,met):
    frequent_itemsets = apriori(bsets, min_support=minsup, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric=met, min_threshold=1)
    return rules




