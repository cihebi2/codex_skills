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

with open('demo_66d12450e4241f11dffdab3d_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_66d12450e4241f11dffdab3d_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '66d12450e4241f11dffdab3d', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'sample',
        'groupCol':'category',
        'valueCols':'v1、v2、v3、v4、v5、v6',
        'showTxtCol':'vnames',
        'legendShowCol':'show',
        'ytitle':'',
    }
}

NgplotApiFun(ngplotPostData,'test')
