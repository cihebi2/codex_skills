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

with open('demo_66cdcef3bf89ff2f8e8cadbd_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_66cdcef3bf89ff2f8e8cadbd_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '66cdcef3bf89ff2f8e8cadbd', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'groupCol':'group',
        'linex1VCol':'x1',
        'liney1VCol':'y1',
        'linex2VCol':'x2',
        'liney2VCol':'y2',
        'areaBaseVCol':'lower',
        'areaPosVCol':'x',
        'areaJumpVCol':'upper',
        'xtitle':'',
        'ytitle':'',
    }
}

NgplotApiFun(ngplotPostData,'test')
