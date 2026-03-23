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

with open('demo_680aeef4a0e69348b047ffd0_data1.txt') as fr:
    datas['data1'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '680aeef4a0e69348b047ffd0', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'xVCol':'log2FoldChange',
        'yVCol':'pvalue',
        'idCol':'id',
        'leftSplitValue':'-1',
        'rightSplitValue':'1',
        'horizontalSplitValue':'0.05',
        'nameShowUpthreshold':'1.3',
        'txtShowNum':'10',
        'xTitle':'logFC',
    }
}

NgplotApiFun(ngplotPostData,'test')
