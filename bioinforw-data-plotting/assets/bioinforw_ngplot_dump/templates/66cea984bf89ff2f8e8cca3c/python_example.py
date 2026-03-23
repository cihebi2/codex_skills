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

with open('demo_66cea984bf89ff2f8e8cca3c_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_66cea984bf89ff2f8e8cca3c_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '66cea984bf89ff2f8e8cca3c', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'name',
        'valueCols':'a、b',
        'pValCol':'P',
        'pName1Col':'n1',
        'pName2Col':'n2',
        'txtVarNames':'a、b、v1、v2、v3',
        'txtShowNames':'Test group、CK group、AAAAAAA、BBBBB、CCCC',
        'txtShowAdd':'、、aaaa、bbbb、 cccc',
        'ytitle':' ',
        'title':'Title ( % )',
    }
}

NgplotApiFun(ngplotPostData,'test')
