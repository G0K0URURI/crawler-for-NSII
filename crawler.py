from PyQt5.QtCore import QThread, pyqtSignal
import requests
import time
import json


class Thread_1(QThread):  # 线程1
    _signal = pyqtSignal(str)

    def __init__(self, name_file, location_file, error_file, specimen_file):
        super().__init__()
        self.names = open(name_file, 'r', encoding='UTF-8').readlines()
        self.location_file = location_file
        self.error_file = error_file
        self.specimen_file = specimen_file

    def run(self):
        with open(self.location_file, 'w', encoding='UTF-8') as f:
            f.write('物种名\t省\t市\t县\t经度\t纬度\t行政区划代码\r')
        with open(self.specimen_file, 'w', encoding='UTF-8') as f:
            f.write('中文名\t学名\t采集地\t属名\t采集人\t种名\t科名\r')
        with open(self.error_file, 'w', encoding='UTF-8') as f:
            f.write('物种名\t采集地\r')
        for name in self.names:
            name = name.replace('\r', '')
            name = name.replace('\n', '')
            self.query_specimen(name)
        self._signal.emit('查找完成')

    def get_url(self, name, start):
        name = name.replace(' ', '%20')
        url = 'http://159.226.89.37/API/NSIISpecimenAgent2.ashx?q=names:%22' + name + \
              '%22%20AND%20hasimage:%221%22&wt=json&facet.field=family&facet.field=countryiso&facet.field=kingdom&start=' \
              + str(start)
        return url

    def indexstr(self, str1, str2):
        # 查找指定字符串str1包含指定子字符串str2的全部位置，以列表形式返回
        len2 = len(str2)
        len1 = len(str1)
        indexstr2 = []
        i = 0
        while str2 in str1[i:]:
            indextmp = str1.index(str2, i, len1)
            indexstr2.append(indextmp)
            i = (indextmp + len2)
        return indexstr2

    def find_distribution(self, s, loc_list, name):
        # 获取标准化县级分布地、经纬度，并对地名去重
        index = self.indexstr(s, "lessgeo")
        error_num = 0
        matching_num = 0  # 分布地精度为县级或以上的标本个数
        for i in index:
            j = s.find('"', i + 10)
            # print(s[index[i]+10:j])
            # deal_with_distribution(s[index[i]+10:j])
            location = s[i + 10:j]
            location = location.replace(';', '')
            location = location.replace('省', '')
            location = location.replace('市', '')
            location = location.replace('县', '')
            location = location.replace(' ', '')
            if location != '':
                try:
                    _url = 'https://restapi.amap.com:443/v3/geocode/geo?address={}&output=JSON&key=716198a26d77ecbe1a5b983c32f88272'.format(location)
                    response = json.loads(requests.get(_url, timeout=5).text)
                except requests.exceptions.RequestException as e:
                    self._signal.emit('connection error!')
                else:
                    if response['status'] == '0':
                        self._signal.emit(response['info'])
                        with open(self.error_file, 'a', encoding='UTF-8') as f:
                            f.write(name + '\t' + location + '\r')
                        error_num += 1
                    elif len(response["geocodes"]) == 0:
                        with open(self.error_file, 'a', encoding='UTF-8') as f:
                            f.write(name + '\t' + location + '\r')
                        error_num += 1
                    else:
                        data = response['geocodes'][0]
                        if data['level'] == '区县' or data['level'] == '兴趣点':
                            province = data['province']
                            city = data['city']
                            if len(city) == 0:
                                city = ' '
                            district = data['district']
                            location = data['location'].split(',', 1)
                            adcode = data['adcode']
                            if adcode not in loc_list:
                                with open(self.location_file, 'a', encoding='UTF-8') as f:
                                    f.write(name + '\t' + province + '\t' + city + '\t' + district + '\t' + location[0]
                                            + '\t' + location[1] + '\t' + adcode + '\r')
                                loc_list.append(adcode)
                            matching_num += 1
        return len(index), matching_num, error_num, loc_list

    def find_number(self, s):
        # 获取标本总数
        index = s.index("numFound")
        j = s.find(',', index)
        return s[index+10:j]

    def find_inf(self, s):
        # 获取所有标本信息
        index = self.indexstr(s, 'text')
        for i in index:
            j = s.find(']', i)
            text = s[i+7:j]
            text = text.replace('","', '\t')
            text = text.replace('"', '')
            with open(self.specimen_file, 'a', encoding='UTF-8') as f:
                f.write(text+'\r')

    def query_specimen(self, name):
        self._signal.emit('正在爬取' + name + '标本信息')
        start = 0
        num = 0
        matching_num_sum = 0
        error_num_sum = 0
        loc_list = []
        while start == num:
            t = 0  # 尝试连接的次数
            while t < 5:
                url = self.get_url(name, start)
                try:
                    res = requests.get(url, timeout=5)
                    break
                except requests.exceptions.ConnectionError:
                    self._signal.emit('ConnectionError -- please wait 3 seconds')
                    t = t + 1
                    time.sleep(3)
                except requests.exceptions.ChunkedEncodingError:
                    self._signal.emit('ChunkedEncodingError -- please wait 3 seconds')
                    t = t + 1
                    time.sleep(3)
                except:
                    self._signal.emit('Unfortunately -- An Unknown Error Happened, Please wait 3 seconds')
                    t = t + 1
                    time.sleep(3)
            if t < 5:
                s = res.text
                self._signal.emit(str(start)+'/'+self.find_number(s))
                (specimen_num, matching_num, error_num, loc_list) = self.find_distribution(s, loc_list, name)
                self.find_inf(s)
                num = num + specimen_num
                matching_num_sum += matching_num
                error_num_sum += error_num
                start = start + 10
            else:
                self._signal.emit('爬取' + name + '标本信息时出现异常')
                # error_file.write(name + '\r')
                return
        self._signal.emit(name + '共有' + str(num) + '条标本信息，共有' + str(matching_num_sum) +
                                   '条标本采集地信息分布地精度为县级或以上，共有' + str(error_num_sum) + '条错误采集地信息')
