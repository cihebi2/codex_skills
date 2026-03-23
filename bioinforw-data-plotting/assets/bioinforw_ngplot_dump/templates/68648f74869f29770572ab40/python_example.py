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

with open('demo_68648f74869f29770572ab40_data1.txt') as fr:
    datas['data1'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '68648f74869f29770572ab40', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'sourceCol':'group1',
        'targetCol':'group2',
        'weightVCol':'Weight',
        'pVCol':'pvalue',
        'pSection':'0.001、0.01、0.05',
        'weightSection':'auto',
    }
}

NgplotApiFun(ngplotPostData,'test')
