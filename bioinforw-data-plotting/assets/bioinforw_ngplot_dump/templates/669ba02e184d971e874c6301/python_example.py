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

with open('demo_669ba02e184d971e874c6301_data1.txt') as fr:
    datas['data1'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '669ba02e184d971e874c6301', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'组别',
        'valueCols':'A、B',
        'sdVCols':'Asd、Bsd',
        'xtitle':'xxxxxxx',
        'ytitle':'yyyyyyy',
    }
}

NgplotApiFun(ngplotPostData,'test')
