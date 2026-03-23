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

with open('demo_67da4f8bf4b5713b590f4c60_data1.txt') as fr:
    datas['data1'] = fr.read()


with open('demo_67da4f8bf4b5713b590f4c60_data2.txt') as fr:
    datas['data2'] = fr.read()



ngplotPostData = {
    'account': 'cihebi',  #
    'ngplotApiKey': '' , #your ngplotApiKey
    'template' : '67da4f8bf4b5713b590f4c60', # template id
    'data' : datas,
    'arg' : { 
        ##params 
        'groupCol':'fertilizer',
        'xVCol':'height',
        'yVCol':'stem_diameter',
        'axis1dot1Col':'Point1',
        'axis1dot2Col':'Point2',
        'axis2dot1Col':'Point3',
        'axis2dot2Col':'Point4',
    }
}

NgplotApiFun(ngplotPostData,'test')
