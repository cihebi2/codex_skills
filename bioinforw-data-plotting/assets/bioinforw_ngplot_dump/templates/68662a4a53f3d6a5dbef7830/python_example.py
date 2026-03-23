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

with open('demo_666a9c36698df4eebb5a9f81_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_666a9c36698df4eebb5a9f81_data2.txt') as fr:
    datas['data2'] = fr.read()


with open('demo_666a9c36698df4eebb5a9f81_data3.txt') as fr:
    datas['data3'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '666a9c36698df4eebb5a9f81', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'name',
        'valueCols':'a、b、c',
        'sdCols':'a_sd、b_sd、c_sd',
        'pValCol':'p',
        'pName1Col':'n1',
        'pName2Col':'n2',
        'dotSubNameCol':'n',
        'dotValCol':'sample',
    }
}

NgplotApiFun(ngplotPostData,'test')
