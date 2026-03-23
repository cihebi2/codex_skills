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

with open('demo_667cdfd87addf6468a7b5f66_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_667cdfd87addf6468a7b5f66_data2.txt') as fr:
    datas['data2'] = fr.read()


with open('demo_667cdfd87addf6468a7b5f66_data3.txt') as fr:
    datas['data3'] = fr.read()


with open('demo_667cdfd87addf6468a7b5f66_data4.txt') as fr:
    datas['data4'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '667cdfd87addf6468a7b5f66', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'groupCol':'group',
        'xVCol':'x',
        'yVCol':'y',
        'linex1VCol':'x1',
        'liney1VCol':'y1',
        'linex2VCol':'x2',
        'liney2VCol':'y2',
        'areaBaseVCol':'lower',
        'areaPosVCol':'x',
        'areaJumpVCol':'upper',
    }
}

NgplotApiFun(ngplotPostData,'test')
