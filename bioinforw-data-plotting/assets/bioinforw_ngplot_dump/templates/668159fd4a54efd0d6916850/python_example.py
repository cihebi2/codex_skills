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

with open('demo_668159fd4a54efd0d6916850_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_668159fd4a54efd0d6916850_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '668159fd4a54efd0d6916850', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'name',
        'dotCol':'dotValue',
        'minVCol':'Min',
        'q1VCol':'Q1',
        'midVCol':'Q2',
        'q3VCol':'Q3',
        'maxVCol':'Max',
        'markCol':'mark',
        'yTtitle':'xxxxxxxxxxx',
    }
}

NgplotApiFun(ngplotPostData,'test')
