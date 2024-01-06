import pandas as pd
import time,datetime
import pathlib
from sklearn.ensemble import RandomForestClassifier
import json
cwd = pathlib.Path.cwd()
rel = pd.read_csv(cwd / 'data' / 'rel.csv', index_col=0)
road = pd.read_csv(cwd / 'data' / 'road.csv', index_col=0)
traj = pd.read_csv(cwd / 'data' / 'traj.csv', index_col=0)
eta = pd.read_csv(cwd / 'data' /'eta_task.csv', index_col=0)
jump = pd.read_csv(cwd / 'data' / 'jump_task.csv', index_col=0)
node = pd.read_csv(cwd / 'data' / 'node.csv', index_col=0)
df = traj#数据预处理
columns = list(df.columns)
tjtm= df[columns[0]].tolist()
model= RandomForestClassifier()
columns = list(df.columns)
tjid = df[columns[2]].tolist()
tjtm= df[columns[0]].tolist()
tjps=df[columns[3]].tolist()
tjhd=df[columns[6]].tolist()
t=tjid[0]
Y=[]
X=[]
X.append([])
temdata = json.loads(tjps[0]) #坐标读入
X[0].append(temdata[0])
X[0].append(temdata[1])
k = 0
while tjtm[0][k] != 'Z':    #时间转化为打他time格式
    if tjtm[0][k] == 'T':
        tjtm[0] = tjtm[0][0:k] + ' ' + tjtm[0][k + 1:-1]
        break
    k = k + 1
timebg = datetime.datetime.strptime(tjtm[0], "%Y-%m-%d %H:%M:%S")
j=0
size= len(tjid)
print(size)
for i in range(1,size-1):
    if tjid[i]!=t:
        temdata = json.loads(tjps[i - 1])
        X[j].append(temdata[0])
        X[j].append(temdata[1])
        t = tjid[i]
        X[j].append(tjhd[i - 1])
        k = 0
        while tjtm[i - 1][k] != 'Z':
            if tjtm[i - 1][k] == 'T':
                tjtm[i - 1] = tjtm[i - 1][0:k] + ' ' + tjtm[i - 1][k + 1:-1]
                break
            k = k + 1
        timeed = datetime.datetime.strptime(tjtm[i - 1], "%Y-%m-%d %H:%M:%S")
        diff = timeed - timebg
        Y.append(diff.total_seconds())
        j = j + 1
        X.append([])
        temdata = json.loads(tjps[i])
        X[j].append(temdata[0])
        X[j].append(temdata[1])
        k = 0
        while tjtm[i][k] :
            if tjtm[i][k] == 'T':
                tjtm[i] = tjtm[i][0:k] + ' ' + tjtm[i][k + 1:-1]
                break
            k = k + 1
        timebg = datetime.datetime.strptime(tjtm[i], "%Y-%m-%d %H:%M:%S")
temdata = json.loads(tjps[size - 1])
X[j].append(temdata[0])
X[j].append(temdata[1])
X[j].append(tjhd[size - 1])
k = 0
while tjtm[size - 1][k] != 'Z':
    if tjtm[size - 1][k] == 'T':
        tjtm[size - 1] = tjtm[size - 1][0:k] + ' ' + tjtm[size - 1][k + 1:-1]
        break
    k = k + 1
timeed = datetime.datetime.strptime(tjtm[size - 1], "%Y-%m-%d %H:%M:%S")
diff = timeed - timebg
Y.append(diff.total_seconds())
columns = list(eta.columns)
tjid = eta[columns[2]].tolist()
tjps=eta[columns[3]].tolist()
tjhd=eta[columns[3]].tolist()
t=tjid[0]
X_test=[]
j=0
size= len(tjid)
for i in range(0,size-1):  #eta预测数据预处理
    if i%2==0:
        X_test.append([])
        temdata=json.loads(tjps[i])
        X_test[j].append(temdata[0])
        X_test[j].append(temdata[1])
    else:
        temdata = json.loads(tjps[i-1])
        X_test[j].append(temdata[0])
        X_test[j].append(temdata[1])
        t=tjid[i]
        X_test[j].append(tjhd[i-1])
        j=j+1

model.fit(X, Y)
predicted= model.predict(X_test)
res=pd.DataFrame(columns=['Estimate'],data=predicted)
res.to_csv('rest.csv')
