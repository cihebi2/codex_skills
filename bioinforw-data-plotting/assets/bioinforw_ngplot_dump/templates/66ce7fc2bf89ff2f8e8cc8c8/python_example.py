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

with open('demo_66ce7fc2bf89ff2f8e8cc8c8_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_66ce7fc2bf89ff2f8e8cc8c8_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '66ce7fc2bf89ff2f8e8cc8c8', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'nameCol':'name',
        'valueCols':'a、b',
        'pValCol':'P',
        'pName1Col':'n1',
        'pName2Col':'n2',
        'per1Cols':'a2、b2',
        'per2Cols':'a1、b1',
        'txtVarNames':'a、b、v1、v2、v3',
        'txtShowNames':'Test group、CK group、AAAAAAA、BBBBB、CCCC',
        'txtShowAdd':'、、aaaa、bbbb、 cccc',
        'ytitle':' ',
        'title':'Title',
    }
}

NgplotApiFun(ngplotPostData,'test')
