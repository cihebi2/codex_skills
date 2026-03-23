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

with open('demo_675985a1646e71bae4dd3f70_data1.txt') as fr:
    datas['data1'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '675985a1646e71bae4dd3f70', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'picCol':'age',
        'nameCol':'name',
        'valueCol':'Mean',
        'sdCols':'SD',
        'yTitle':'',
        'minVs':'0、0、0、0',
        'maxVs':'100、100、100、100',
        'steps':'20、20、20、20',
    }
}

NgplotApiFun(ngplotPostData,'test')
