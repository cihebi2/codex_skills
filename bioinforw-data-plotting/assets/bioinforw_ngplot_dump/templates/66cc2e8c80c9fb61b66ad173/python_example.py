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

with open('demo_66cc2e8c80c9fb61b66ad173_data1.txt') as fr:
    datas['data1'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '66cc2e8c80c9fb61b66ad173', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'Sample',
        'groupCol':'group',
        'title':'XXXXXXX',
        'minv':'auto',
        'maxv':'auto',
        'step':'auto',
    }
}

NgplotApiFun(ngplotPostData,'test')
