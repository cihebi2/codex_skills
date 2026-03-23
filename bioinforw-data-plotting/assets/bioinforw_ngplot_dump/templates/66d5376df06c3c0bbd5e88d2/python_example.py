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

with open('demo_6758eb7cb309cfee57d3c697_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_6758eb7cb309cfee57d3c697_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '6758eb7cb309cfee57d3c697', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'VarName',
        'valueCols':'A、B',
        'sdCols':'Asd、Bsd',
        'pValCol':'pValue',
        'pName1Col':'n1',
        'pName2Col':'n2',
        'step':'0.2',
        'yRange':'0,1.1;2.9,3.6',
        'ytitle':'YYYYYYYYY',
    }
}

NgplotApiFun(ngplotPostData,'test')
