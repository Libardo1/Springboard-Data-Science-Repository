
# Written by Zachary Kneupper
# 2017-08-24

# This program was written to wrangle/clean data in
# 'default of credit card clients.csv' and to export the
# wrangled/cleaned data data to a new file called 
# 'default of credit card clients - wrangled.csv'
# and a second wrangled/cleaned with outliers removed called
# 'default of credit card clients - wrangled - trimmed.csv'



import pandas as pd
import numpy as np

df = pd.read_csv('default of credit card clients.csv', header=1, index_col=0)


####################################################################################
####################################################################################

# Check for any null values in the dataset.
# If df.isnull().values.any() returns False, then there are no null values.
df.isnull().values.any()

# RETURNS False

####################################################################################
####################################################################################

# Create functiond to inspect variables

def inspect_discrete_var(input_series=None, accepted_values_list=None):
    
    """ Docstring: inspect discrete variable
    
    The argument of the function "input_series" should be a pandas Series object.
    
    The function returns a pandas Styler object "output_styler".
    
    Rows for values not in accepted_values_list will be colored red.
    
    "output_styler" can be turned in to a Dataframe Object by calling
    the .data method (output_styler.data or inspect_discrete_var_2(arg).data).
    """
    
    try:
        temp = input_series.value_counts()
        temp.sort_index(ascending=True, inplace=True)
        temp.sort_index()
        temp.index.name = temp.name
        temp.rename('value_counts', inplace=True)
        n = len(input_series)
        temp_percent = temp / n
        temp_percent.rename('percentage', inplace=True)
        temp_percent
        temp_df = temp.to_frame().join(temp_percent.to_frame())
        
        temp_styler =  temp_df.style.format({'value_counts': '{:,}', 'percentage': '{:,.1%}'})

        styles = []
        
        try:

            for row, item in enumerate(temp_styler.index, start=0): 
                if item not in accepted_values_list:
                    styles.append({'selector': '.row'+str(row),
                                   'props': [('background-color', 'red'), 
                                             ('color', 'white'),
                                             ('font-weight', 'bold')]})
        except:
            pass                    
                    
        #return my_styles
        
        return temp_styler.set_table_styles(styles)
    except:
        # Return exception
        return None

def inspect_continuous_var(input_series=None):
    
    """ Docstring: inspect continuous variable
    
    The argument of the function "input_series" should be a pandas Series object.
    
    The function returns summary plots and summary statistics.
            
    """

    # Display boxplot and histogram/kde.
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 5) )
    sns.boxplot(x=input_series, ax=ax1)
    sns.distplot(input_series, ax=ax2)
    font = {'weight' : 'bold',
            'size'   : 16}
    ax1.set_title(input_series.name, fontdict=font)
    plt.show()

    # Print summary statistics.
    print('Min: \t\t\t {:,.0f}'.format(input_series.min()))
    print('Lower Quartile: \t {:,.0f}'.format(input_series.quantile([.25]).iloc[0]))
    print('median: \t\t {:,.0f}'.format(input_series.median()))
    print('mean: \t\t\t {:,.0f}'.format(input_series.mean()))
    print('Upper Quartile: \t {:,.0f}'.format(input_series.quantile([.75]).iloc[0]))                                    
    print('max: \t\t\t {:,.0f}'.format(input_series.max()))
    print('\n')
    print('Skew: \t\t\t {:,.2f}'.format(input_series.skew()))
    print('Kurtosis: \t\t {:,.2f}'.format(input_series.kurtosis()))

    return None

####################################################################################
####################################################################################

def trim(x, trim_max=None, trim_min=None):
    """ Docstring: Trim outliers below trim_min or above trim_max.
    """
    if ((trim_max != None) & (trim_min != None)):
        if x > trim_max:
             return trim_max
        else:
            if x < trim_min:
                return trim_min
            else:
                return x
            
    elif (trim_max != None): 
        if x > trim_max:
             return trim_max
        else:
            return x

    elif (trim_min != None): 
        if x < trim_min:
             return trim_min
        else:
            return x
        
    else:
        return x

####################################################################################
####################################################################################
# WRANGLE DATA
####################################################################################
####################################################################################

# The dependent variable ('default payment next month') is imbalanced.

# 77.9% of the observations do not default in the next month 
#    ('default payment next month' = 0).

# 22.1% of the observations do default in the next month 
#    ('default payment next month' = 1).

# The data set may need to be rebalanced / resampled.

####################################################################################
####################################################################################

# No data wrangling is needed for 'SEX'.

####################################################################################
####################################################################################

# Reassign 'EDUCATION' values not in [1, 2, 3, 4] to 4 (4 = others).

def reassign_EDUCATION(x):
    
    accepted_values_list = [1, 2, 3, 4]

    if x in accepted_values_list:
        output = x
    else:
        output = 4
        
    return output
        
df_edited = df.copy()

df_edited['EDUCATION'] = df_edited.EDUCATION.apply(reassign_EDUCATION)

# 'EDUCATION' data has been wrangled.

####################################################################################
####################################################################################

# No data wrangling is needed for 'MARRIAGE'.

####################################################################################
####################################################################################

# No data wrangling is needed for 'PAY_0', 'PAY_2', 'PAY_3',
# 'PAY_4', 'PAY_5', and 'PAY_6'.

# We relabel 'PAY_0' as 'PAY_1'.

df_edited.rename(columns={'PAY_0': 'PAY_1'}, inplace=True)

####################################################################################
####################################################################################

# 'LIMIT_BAL' has high kurtosis and is highly skewed. 
# We will create a second edited data set
# in which we trim outliers.

df_edited_trimmed = df_edited.copy()

trim_max = df_edited_trimmed.LIMIT_BAL.quantile(.75)
df_edited_trimmed.LIMIT_BAL = df_edited_trimmed.LIMIT_BAL.apply(trim, 
                                                                trim_max=trim_max)

####################################################################################
####################################################################################

# No data wrangling is needed for 'AGE'.

####################################################################################
####################################################################################

# 'BILL_AMT1' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.BILL_AMT1.quantile(.75)
trim_min = df_edited_trimmed.BILL_AMT1.quantile(.25)
df_edited_trimmed.BILL_AMT1 = df_edited_trimmed.BILL_AMT1.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# 'BILL_AMT2' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.BILL_AMT2.quantile(.75)
trim_min = df_edited_trimmed.BILL_AMT2.quantile(.25)
df_edited_trimmed.BILL_AMT2 = df_edited_trimmed.BILL_AMT2.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)


####################################################################################
####################################################################################

# 'BILL_AMT3' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.BILL_AMT3.quantile(.75)
trim_min = df_edited_trimmed.BILL_AMT3.quantile(.25)
df_edited_trimmed.BILL_AMT3 = df_edited_trimmed.BILL_AMT3.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# 'BILL_AMT4' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.BILL_AMT4.quantile(.75)
trim_min = df_edited_trimmed.BILL_AMT4.quantile(.25)
df_edited_trimmed.BILL_AMT4 = df_edited_trimmed.BILL_AMT4.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# 'BILL_AMT5' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.BILL_AMT5.quantile(.75)
trim_min = df_edited_trimmed.BILL_AMT5.quantile(.25)
df_edited_trimmed.BILL_AMT5 = df_edited_trimmed.BILL_AMT5.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# 'BILL_AMT6' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.BILL_AMT6.quantile(.75)
trim_min = df_edited_trimmed.BILL_AMT6.quantile(.25)
df_edited_trimmed.BILL_AMT6 = df_edited_trimmed.BILL_AMT6.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# 'PAY_AMT1' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.PAY_AMT1.quantile(.75)
trim_min = df_edited_trimmed.PAY_AMT1.quantile(.25)
df_edited_trimmed.PAY_AMT1 = df_edited_trimmed.PAY_AMT1.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# 'PAY_AMT2' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.PAY_AMT2.quantile(.75)
trim_min = df_edited_trimmed.PAY_AMT2.quantile(.25)
df_edited_trimmed.PAY_AMT2 = df_edited_trimmed.PAY_AMT2.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# 'PAY_AMT3' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.PAY_AMT3.quantile(.75)
trim_min = df_edited_trimmed.PAY_AMT3.quantile(.25)
df_edited_trimmed.PAY_AMT3 = df_edited_trimmed.PAY_AMT3.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# 'PAY_AMT4' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.PAY_AMT4.quantile(.75)
trim_min = df_edited_trimmed.PAY_AMT4.quantile(.25)
df_edited_trimmed.PAY_AMT4 = df_edited_trimmed.PAY_AMT4.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# 'PAY_AMT5' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.PAY_AMT5.quantile(.75)
trim_min = df_edited_trimmed.PAY_AMT5.quantile(.25)
df_edited_trimmed.PAY_AMT5 = df_edited_trimmed.PAY_AMT5.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# 'PAY_AMT6' has high kurtosis and is highly skewed. 
# We will trim these outliers in df_edited_trimmed.

trim_max = df_edited_trimmed.PAY_AMT6.quantile(.75)
trim_min = df_edited_trimmed.PAY_AMT6.quantile(.25)
df_edited_trimmed.PAY_AMT6 = df_edited_trimmed.PAY_AMT6.apply(trim, 
                                                                trim_max=trim_max,
                                                                trim_min=trim_min)

####################################################################################
####################################################################################

# Export edited DataFrame to new csv file

temp_df = pd.read_csv('default of credit card clients.csv')
header_list = list(temp_df.columns)
header_list[0] = ''

df_edited_2 = df_edited.copy()
df_edited_2.reset_index(inplace=True)

arrays = [header_list, list(df_edited_2.columns)]
df_edited_2.columns = arrays

df_edited_2.to_csv('default of credit card clients - wrangled.csv', index=False)


####################################################################################
####################################################################################


temp_df = pd.read_csv('default of credit card clients.csv')
header_list = list(temp_df.columns)
header_list[0] = ''

df_edited_trimmed_2 = df_edited_trimmed.copy()
df_edited_trimmed_2.reset_index(inplace=True)

arrays = [header_list, list(df_edited_trimmed_2.columns)]
df_edited_trimmed_2.columns = arrays

df_edited_trimmed_2.to_csv('default of credit card clients - wrangled - trimmed.csv', index=False)
