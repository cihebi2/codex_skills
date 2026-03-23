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

with open('demo_6755691a30ab699948765097_data1.txt') as fr:
    datas['data1'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '6755691a30ab699948765097', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'Sample',
        'groupCol':'type',
        'valueCols':'var1、var2、var3',
        'maxv':'400',
        'minv':'0',
        'step':'100',
    }
}

NgplotApiFun(ngplotPostData,'test')
