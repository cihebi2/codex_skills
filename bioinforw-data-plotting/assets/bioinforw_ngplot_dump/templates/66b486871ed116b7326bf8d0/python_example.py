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

with open('demo_66b486871ed116b7326bf8d0_data1.txt') as fr:
    datas['data1'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '66b486871ed116b7326bf8d0', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'xVCol':'x',
        'yVCol':'y',
        'x1':'29',
        'y1':'0.18',
        'x2':'1',
        'y2':'0.61',
        'r':'r = xx',
        'p':'p = xx',
        'yTxtN':'1',
        'ytitle':'yyyy',
        'xtitle':'xxxx',
    }
}

NgplotApiFun(ngplotPostData,'test')
