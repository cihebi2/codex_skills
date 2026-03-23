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

with open('demo_68662c1553f3d6a5dbef79e5_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_68662c1553f3d6a5dbef79e5_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '68662c1553f3d6a5dbef79e5', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'sourceCol':'source	',
        'targetCol':'target	',
        'valueCol':'corr',
        'weightVCol':'Weight',
        'rowCol':'col',
        'colCol':'row',
        'xinVCol':'p',
        'pVCol':'pvalue',
        'pSection':'0.001、0.01、0.05',
        'weightSection':'auto',
    }
}

NgplotApiFun(ngplotPostData,'test')
