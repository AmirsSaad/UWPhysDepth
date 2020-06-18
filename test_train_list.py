from zipfile import ZipFile
import pandas as pd
import numpy as np
import glob


namelist = glob.glob(r'./data/D5/*/*.csv')
data_paths = {
    'rgb' : [name for name in namelist if not 'dep' in name and not 'coord' in name],
    'D'   : [name for name in namelist if 'dep' in name]
}
print(data_paths['rgb'])
print(data_paths['D'])

df = pd.DataFrame(data_paths)
print(df)

train_set = df.sample(frac=0.9, random_state=0)
test_set = df.drop(train_set.index)

train_set.to_csv('train_set.csv',index=False)
test_set.to_csv('test_set.csv',index=False)