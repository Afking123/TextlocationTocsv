import os
import csv
# 获取当前文件夹路径
current_directory = os.getcwd()

# 打印当前文件夹路径
print("当前文件夹路径:", current_directory)

# 列出当前文件夹内的所有文件
files = os.listdir(current_directory)

# 遍历文件夹内的所有文件
for file in files:
    # 如果文件是CSV文件，则读取内容
    if file.endswith('.csv')&(not "_output"in file):
        print("正在读取文件:", file)
        with open(file, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            csvlist_1=[]
            csvlist=[]#裝csv的陣列
            csvlist2=[]#y軸已排好,x軸也排好
            csvlist3=[]#填補空白的部分
            csvlist4=[]#去除xy軸
            #跳過內容,位置 X,位置 Y
            next(csv_reader)
            #輸出至csvlist
            for info in csv_reader:
                csvlist_1.append(info)
            #將不合格式的文字塞入下一段資料
            for row in range(len(csvlist_1)):
                if len(csvlist_1[row])<3:
                    csvlist_1[row+1][0]=str(csvlist_1[row][0]+csvlist_1[row+1][0])
                else:
                    csvlist.append(csvlist_1[row])
            #print(csvlist)
            #csvlist照y軸順序由小到大排列
            for row in range(len(csvlist)):
                csvlist[row][2]=float(csvlist[row][2])
                csvlist[row][1]=float(csvlist[row][1])
            csvlist=sorted(csvlist,key=lambda x: x[2],reverse=True)
            #相同y的塞進csvlist2
            x=0
            i=0
            empty_arry=[]
            for row in csvlist:
                if row[2]==x:
                    empty_arry.append(row)
                else:
                    csvlist2.append(empty_arry)
                    x = row[2]
                    empty_arry=[]
                    empty_arry.append(row)
            del csvlist2[0]
            #同y軸的照x軸大小排列
            j=0
            for row in csvlist2:
                csvlist2[j]=sorted(row,key=lambda x: x[1])
                j+=1
            #取陣列值最多的陣列
            biggestarray =max(csvlist2,key=len)
            #如果陣列有比其他陣列缺，補空格
            for row in csvlist2:
                if len(row)!=len(biggestarray):
                    for rownumber in range(len(biggestarray)):
                        try:
                            if (row[rownumber][1] != biggestarray[rownumber][1]):
                               row.insert(rownumber,["",0,0])
                        except:
                            for i in range(len(biggestarray)-len(row)):
                                row.append(["",0,0])
                    csvlist3.append(row)
                else:
                    csvlist3.append(row)
            #去xy軸
            emptyarry=[]
            for row in csvlist3:
                for rowrow in row:
                    emptyarry.append(rowrow[0])
                csvlist4.append(emptyarry)
                emptyarry=[]
            
            

        output_filename=os.path.splitext(file)[0]+"_output"+".csv"
        with open(output_filename, 'w', newline='', encoding='utf-8') as output_csvfile:
            csv_writer = csv.writer(output_csvfile)
            csv_writer.writerows(csvlist4)
        print("已輸出文件:"+output_filename)