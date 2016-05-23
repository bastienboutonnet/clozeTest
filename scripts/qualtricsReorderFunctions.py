import pandas as pd
import numpy as np

def melt_df_feed_info_from_loop_merge():
    #MELT
    col_names=pd.Series(df.columns)
    valid_cols_mask=col_names.str.contains(colsToPull,regex=True)
    valid_cols = df.columns[valid_cols_mask]
    df=df[valid_cols]
    df=pd.melt(df,id_vars='subj_id',var_name='qual_col',value_name=measureName)

    #Extract useful information from qual_cols
    qualtrics_parsed=df.qual_col.str.extract('^(?P<measure>\w+)\((?P<row>\d+)\)$')
    qualtrics_parsed = qualtrics_parsed.convert_objects(convert_numeric=True)
    df = pd.concat([df, qualtrics_parsed], axis = 1)
    df = df.merge(loopmergeInfo, how='left')

    return df

def reconstruct_order_and_melt_with_df():
    variables=loopmergeInfo.Name.as_matrix()
    order_split=ord.preorder.str.split("|")

    for v in variables:
        ord[v] = order_split.apply(lambda x: x.index(v) + 1)

    order=ord.drop(['preorder'],axis=1)
    #MELT ORDER
    order=pd.melt(order,id_vars='subj_id',var_name='Name',value_name='position')

    #MERGE WITH DF
    datNorder=pd.merge(df,order,how='left',on=['Name','subj_id'])

    return datNorder





if __name__=='__main__':
    df=pd.read_csv("SomeFile.csv",skiprows=[1,])
    df=df.rename(columns={df.columns[0]:'subj_id'})
    loopmergeInfo=pd.read_csv("SomeLoopmerge.csv")
    ord=df[['subj_id','preorder']]

    colsToPull='^subj_id|Q' #whatever regEx works
    measureName="RT"

    recDF=melt_df_feed_info_from_loop_merge()
    #recDForder=reconstruct_order_and_melt_with_df()
