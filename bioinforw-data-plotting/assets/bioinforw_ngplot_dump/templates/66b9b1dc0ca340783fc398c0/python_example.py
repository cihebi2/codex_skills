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

with open('demo_66b9b1dc0ca340783fc398c0_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_66b9b1dc0ca340783fc398c0_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '66b9b1dc0ca340783fc398c0', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'name',
        'groupCol':'group',
        'minVCol':'Min',
        'q1VCol':'Q1',
        'midVCol':'Q2',
        'q3VCol':'Q3',
        'maxVCol':'Max',
        'bigVCol':'split1New',
        'name2Col':'name',
        'yminV':'-50',
        'ymaxV':'10',
        'ystep':'10',
        'smallVcol':'split0New',
        'ytitle':'',
    }
}

NgplotApiFun(ngplotPostData,'test')
