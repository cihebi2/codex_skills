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

with open('demo_68ff30e4bb52e65911957081_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_68ff30e4bb52e65911957081_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '68ff30e4bb52e65911957081', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'group',
        'groupCol':'group',
        'xVCol':'x',
        'yVCol':'y',
        'linex1VCol':'x1',
        'liney1VCol':'y1',
        'linex2VCol':'x2',
        'liney2VCol':'y2',
        'ytitle':'',
        'xtitle':'',
    }
}

NgplotApiFun(ngplotPostData,'test')
