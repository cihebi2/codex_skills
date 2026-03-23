import requests
import json

def NgplotApiFun(ngplotPostData,svgOutName):
    response = requests.post('https://www.bioinforw.com/ldm/ngplotApiSim/', data={'data':json.dumps(ngplotPostData)})
    if response.status_code == 200:
        response_json = response.json()
        if response_json['code'] == 200:
            with open(svgOutName+'.svg', 'w') as fw:
                fw.write(response_json['svg'])
            print('Success, the result file is '+ svgOutName + '.svg')
        else:
            print(response_json['msg'])

##Test:
datas = {}

with open('demo_66cc7d811cedc4fc9f289534_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_66cc7d811cedc4fc9f289534_data2.txt') as fr:
    datas['data2'] = fr.read()


with open('demo_66cc7d811cedc4fc9f289534_data3.txt') as fr:
    datas['data3'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '66cc7d811cedc4fc9f289534', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'name',
        'valueCols':'mean1',
        'sdCols':'sd1',
        'Name1Col':'n1',
        'Name2Col':'n2',
        'xinCol':'xin',
        'dotsValCol':'value',
        'ytitle':'YYYYYY',
        'xtitle':'',
    }
}

NgplotApiFun(ngplotPostData,'test')
