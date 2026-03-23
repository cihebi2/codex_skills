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

with open('demo_693005ae56824bcc74877b22_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_693005ae56824bcc74877b22_data2.txt') as fr:
    datas['data2'] = fr.read()


with open('demo_693005ae56824bcc74877b22_data3.txt') as fr:
    datas['data3'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '693005ae56824bcc74877b22', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'name',
        'valueCol':'value',
        'minv':'auto',
        'maxv':'auto',
        'step':'auto',
        'groupCol':'var',
        'maxCol':'Max',
        'q3Col':'Q3',
        'q1Col':'Q1',
        'minCol':'Min',
        'midCol':'Q2',
        'densityCol':'density',
        'data1NameCol':'Group',
    }
}

NgplotApiFun(ngplotPostData,'test')
