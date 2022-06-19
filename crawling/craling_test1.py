##### 저장되어있는 파일 읽어오기 #####
### [파일 불러오기] read(): 통째로 가져오기
# f = open('C:/Users/671/Desktop/y/python/crawlingtest/company list/list.txt', 'r')

# data = f.read()
# print(data)

# f.close()


### [데이터를 1줄씩 가져오기] readlines(): 줄 단위로 가져오기
from model.company import CompanyModel

f = open('C:/Users/671/Desktop/y/python/crawlingtest/company list/list.txt', 'r', encoding='utf-8')

lines = f.readlines()
companyList = []

for line in lines:
    #만약에 빈 공백이 나오면 replace 활용하여 공백 없애주기
    #words = line.replace('\n', '').split(';')

    # split: 구분기호(;)에 따라 분리해서 자료 모으기(list type)
    words = line.split(';')
    name = words[0]
    category = words[1]
    country = words[2]
    score = words[3]
    rank2020 = words[4]
    rank2019 = words[5]
    
    company = CompanyModel(name, category, country, score, rank2020, rank2019)
    companyList.append(company)

f.close()


### [불러온 데이터를 가공하여 출력하기]
for c in companyList:
    data = '{0:>3}  {1:<45} {2:0<5} %'.format(c.rank2020, c.name, c.score)
    print(data)

