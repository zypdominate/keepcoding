import pickle
data = {'Bob': '2', 'Caly': '1', 'Amy': '3'}

file_name = 'test_pickle.txt'
with open(file_name,'wb') as fp:
    pickle.dump(data, fp)

with open(file_name,'rb') as fp:
    res = pickle.load(fp)
    print(res)

