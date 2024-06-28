class Univariate():
    def quanQual (dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            #print(columnName)
            if(dataset[columnName].dtype=='O'):
                #print("qual")
                qual.append(columnName)
            else:
                #print("quan")
                quan.append(columnName)
        return quan,qual
        
    def continuous(dataset,quan):
        descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%","Min","Max","IQR","1.5*IQR","Lesser","Greater"], columns=quan)
        for columnName in quan:
            descriptive[columnName]["Mean"]=dataset[columnName].mean()
            descriptive[columnName]["Median"]=dataset[columnName].median()
            descriptive[columnName]["Mode"]=dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"]=dataset.describe()[columnName]["25%"]
            descriptive[columnName]["Q2:50%"]=dataset.describe()[columnName]["50%"]
            descriptive[columnName]["Q3:75%"]=dataset.describe()[columnName]["75%"]
            descriptive[columnName]["99%"]=np.percentile(dataset[columnName],99)
            descriptive[columnName]["Q4:100%"]=dataset.describe()[columnName]["max"]
            descriptive[columnName]["Min"]=dataset[columnName].min()
            descriptive[columnName]["Max"]=dataset[columnName].max()
            descriptive[columnName]["IQR"]=descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5*IQR"]=1.5*descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"]=descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5*IQR"]
            descriptive[columnName]["Greater"]=descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5*IQR"]
        return descriptive
        
    def findOutlierCols(descriptive,quan):
        lesser=[]
        greater=[]
        for columnName in quan:
            if descriptive[columnName]["Min"]<descriptive[columnName]["Lesser"]:
                lesser.append(columnName)
            if descriptive[columnName]["Max"]>descriptive[columnName]["Greater"]:
                greater.append(columnName)
        return lesser,greater

    def replaceOutlier(dataset,descriptive,lesser,greater):
        for columnName in lesser:
            dataset[columnName][dataset[columnName]<descriptive[columnName]["Lesser"]]=descriptive[columnName]["Lesser"]
        for columnName in greater:
            dataset[columnName][dataset[columnName]>descriptive[columnName]["Greater"]]=descriptive[columnName]["Greater"]
        return descriptive
            
    def freqTable(columnName,dataset):
        FreqTable=pd.DataFrame(columns=["Unique_values","Frequency","Relative_Freq","Cumsum"])
        FreqTable["Unique_values"]=dataset[columnName].value_counts().index
        FreqTable["Frequency"]=dataset[columnName].value_counts().values
        FreqTable["Relative_Freq"]=FreqTable["Frequency"]/FreqTable["Unique_values"].count()
        FreqTable["Cumsum"]=FreqTable["Relative_Freq"].cumsum()
        return FreqTable