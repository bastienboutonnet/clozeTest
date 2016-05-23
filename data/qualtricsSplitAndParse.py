
# coding: utf-8

# # Qualtrics Output Reconstruction & Analysis
# ## When Using Loop & Merge
# ### More than 1 List/Block
#
# #### Step 1: Import libraries, load file

def melt_df_feed_info_from_loop_merge(df):

    #MELT | Transpose df into long format
    col_names=pd.Series(df.columns)
    valid_cols_mask=col_names.str.contains(colsToPull,regex=True)
    valid_cols = df.columns[valid_cols_mask]
    df=df[valid_cols]
    df=pd.melt(df,id_vars='subj_id',var_name='qual_col',value_name=measureName)

    #Extract useful information from qual_cols, and merge key info
    qualtrics_parsed=df.qual_col.str.extract('^(?P<measure>\w+)\((?P<row>\d+)\)$')
    qualtrics_parsed = qualtrics_parsed.convert_objects(convert_numeric=True)
    df = pd.concat([df, qualtrics_parsed], axis = 1)
    df = df.merge(loopmergeInfo, how='left')

    return df



# In[1]:

if __name__=='__main__':
    import pandas as pd
    import re

    df=pd.read_csv('./data/rawDat.csv',skiprows=[1,])
    df=df.rename(columns={df.columns[0]:'subj_id'})


    # ####Step 2: Split lists
    # Assuming you have an embeded data variable created by your Qualtrics survey, here `listNb` you can sort your different participants into blocks. This will extract each participant as a row, and since the columns of the other block will be empty you will want to drop those columns so as not to have empty/useless data.
    #
    # You then store it in a dictionary `dic` which you will increment for each list.
    #
    # Because pandas doesn't like to have column labels with the same name, and rightly so, it will add `.X` where `X` is a number to each duplicate column. This is going to be a problem later on when you're trying to match the column index with the sentence/row index from your *loop and merge key*.
    # We therefore incorporate a step where `re.sub()` will delete a specified pattern (regular expression) consisting of everything after and including the `.`.

    # In[2]:

    dic={}
    for curList in xrange(1,5):
        dic[curList]=df.loc[df['listNb']==curList].dropna(1,how='all')
        cols=list(dic[curList].columns.values) #store columns in a list
        new_cols=[re.sub('\..*$', "", elem) for elem in cols] #make the resub go through each element of the list and do its thing
        dic[curList].columns=new_cols #replace columns back in df.


    # ####Step 3: Perform Parsing
    # Here the steps are written in a function that melts and retrieves the information that we care about.
    # This function is then applied in the next code cell to the different dataframes in the dictionary for each list and appends the lists back together.

    # In[3]:




    # In[4]:

    colsToPull='^subj_id|Timing_1'
    measureName='RT'

    for curList in xrange(1,5):
        loopmergeInfo=pd.read_csv('./data/loopmerge'+str(curList)+'.csv')
        if len(dic[curList])>=1:
            if curList==1:
                reconst=melt_df_feed_info_from_loop_merge(dic[curList])
            else:
                reconst=reconst.append(melt_df_feed_info_from_loop_merge(dic[curList]))
        else:
            print('There was no data in list %d') % curList


    # ####Step 4: Save

    # In[5]:

    reconst.head()
    reconst.to_csv('datRT.csv',index=0)


    # ####Step 4: Analyse/Visualise Data

    # So far the analysis is written in R code, it basically consists of sumarising the file by sentence, completion and get a measure of popularity for each participant. These functions from the `ddply` package are likely to be operationalisable in `pandas` but I haven't worked it out yet.
    #
    # Follow up analysis on R (using R script). Maybe this could be analysed using Python too, but at least it works so far.
