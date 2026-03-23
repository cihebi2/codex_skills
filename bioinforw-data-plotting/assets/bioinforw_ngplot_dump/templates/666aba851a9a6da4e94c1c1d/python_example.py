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

with open('demo_666aba851a9a6da4e94c1c1d_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_666aba851a9a6da4e94c1c1d_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '666aba851a9a6da4e94c1c1d', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'name',
        'dotCol':'dots',
        'minVCol':'min',
        'q1VCol':'qdown',
        'midVCol':'mid',
        'q3VCol':'quper',
        'maxVCol':'max',
        'pValCol':'p',
        'pName1Col':'n1',
        'pName2Col':'n2',
    }
}

NgplotApiFun(ngplotPostData,'test')
