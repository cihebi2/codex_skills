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

with open('demo_69367e2a139236dfba8eecce_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_69367e2a139236dfba8eecce_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '69367e2a139236dfba8eecce', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'name',
        'minv':'-1',
        'maxv':'1',
        'step':'0.5',
        'densityCol':'density',
        'valueCol':'value',
    }
}

NgplotApiFun(ngplotPostData,'test')
