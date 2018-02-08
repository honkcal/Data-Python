import traceback
import requests
import json
##coding:utf-8
import urllib.request
import re
import pyodbc
import time
import os


if __name__ == '__main__':
    try:

        print("connection build")
        conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 10.0};SERVER=;DATABASE=;UID=;PWD=')
        cursor = conn.cursor()
        print("connection build111")

        questjson = '{"query": "\\nquery ins($state: String, $q: String, $include_not_ranked: Boolean, $field_of_study_ranking_key: String, $ranking_key: String, $china_degree: String, $country: String, $field_of_study: String, $offset: Int,$institute_quality:[String],$public_or_private:[String],$institute_type: String,$china_belong_to:[String]) {\\n  institute {\\n      search(state: $state, q: $q, include_not_ranked: $include_not_ranked, field_of_study_ranking_key: $field_of_study_ranking_key, ranking_key: $ranking_key, china_degree: $china_degree, country: $country, field_of_study: $field_of_study, offset: $offset,size:7000,institute_quality: $institute_quality, public_or_private: $public_or_private, institute_type: $institute_type,china_belong_to: $china_belong_to) {\\n  items {\\n   id\\n   slug\\n   name\\n  logo_url\\n          country\\n          country_data\\n  state\\n   city_data\\n      city\\n   ranking {\\n   applysq\\n  arwu\\n   qs\\n  times\\n  usnews\\n    usnews_global\\n      usnews_school_medical_research\\n\\t\\t  }\\n\\t\\t  field_of_study{\\n   accounting {\\n\\t\\t\\t\\t\\t\\t\\tranking{\\n\\t\\t\\t\\t\\t\\t\\t\\tcn\\n\\t\\t\\t\\t\\t\\t\\t\\tapplysq\\n\\t\\t\\t\\t\\t\\t\\t\\tglobal\\n\\t\\t\\t\\t\\t\\t\\t}\\n\\t\\t\\t\\t\\t\\t}\\n  }\\n  wikipedia {\\n   localized_name {\\n  cn\\n   en\\n    }\\n   }\\n  }\\n   page_info {\\n  count\\n   }\\n  }\\n  }\\n  }", "variables": {"q": null, "country": null, "state": null, "china_degree": null, "field_of_study": null,  "include_not_ranked": true, "ranking_key": "qs", "offset": 0}}'
        headers = {'Referer': 'https://www.applysquare.com/ranking-cn',
                   'X-CSRFToken': '064dSTdioTFkYAw81iEGj8vCHYtF8egK'}
        cookies = dict(csrftoken='064dSTdioTFkYAw81iEGj8vCHYtF8egK')

        j = requests.post('https://www.applysquare.com/ajax/graphql', data=questjson, headers=headers,
                          cookies=cookies).json()


        print("-------done extract-------")


        i = 0
        for val in j['data']['institute']['search']['items']:
            chinese_name = (val['wikipedia']['localized_name']['cn'])
            english_name = (val['wikipedia']['localized_name']['en'])
            state = (val['state'])
            country_data = (val['country_data'])
            id = (val['id'])
            rank_qs = str(val['ranking']['qs'])
            rank_times = str(val['ranking']['times'])
            rank_arwu = str(val['ranking']['arwu'])
            logo_url = (val['logo_url'])
            # 分类关键字
            #slug = (val['slug'])
            print(val)
            if(chinese_name is None):
                chinese_name=""
            if (english_name is None):
                english_name = ""
            if (state is None):
                state = ""
            if (logo_url is None):
                logo_url = ""

            i = i + 1
            print("------- 第 " + str(i) + " 个学校 -------")
            # 当前时间信息
            ct = time.time()
            # print(time.time())
            local_time = time.localtime(ct)
            data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            #sql = "INSERT INTO ODS_university_shenqingfang_alllist([university_name])VALUES('" + str(val).replace("'","")+"')"
            #print(chinese_name)

            # 拼出插入University_Master表的sql语句
            sql = "INSERT INTO ODS_university_shenqingfang_master(UniversityName_CN,UniversityName_EN,CountryName,Region,Picture,rank_qs, rank_times,rank_arwu,InsertDate)VALUES('" + \
                  chinese_name.replace("'", "") + "','" + english_name.replace("'", "") + "','" + country_data+ "','" + state.replace("'", "") + "','" +\
                  logo_url.replace("'", "") + "','"+rank_qs.replace("'", "") + "','"+rank_times.replace("'", "") + "','"+rank_arwu.replace("'", "") + "','" + data_head + "')"
            print(chinese_name.replace("'", ""))
            # 执行sql
            cursor.execute(sql)
            # 提交修改
            conn.commit()
            print("-------学校 " + chinese_name.replace("'", "") + " 详细信息采集完成----")


    except :
            traceback.print_exc()

