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

with open('demo_692e4e4beb5ce5e1c52c9a1a_data1.txt') as fr:
    datas['data1'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '692e4e4beb5ce5e1c52c9a1a', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'groupCol':'group',
        'nameCol':'name',
        'valueCol':'value',
        'title':'Title',
    }
}

NgplotApiFun(ngplotPostData,'test')
