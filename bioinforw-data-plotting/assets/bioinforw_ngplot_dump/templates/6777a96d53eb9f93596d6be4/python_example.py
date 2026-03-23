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

with open('demo_6777a96d53eb9f93596d6be4_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_6777a96d53eb9f93596d6be4_data2.txt') as fr:
    datas['data2'] = fr.read()


with open('demo_6777a96d53eb9f93596d6be4_data3.txt') as fr:
    datas['data3'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '6777a96d53eb9f93596d6be4', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'name',
        'valueCol':'value',
        'minVCol':'min',
        'q1VCol':'q1',
        'midVCol':'mid',
        'q3VCol':'q3',
        'maxVCol':'max',
        'densityVCol':'density',
    }
}

NgplotApiFun(ngplotPostData,'test')
