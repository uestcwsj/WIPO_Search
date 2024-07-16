import re
import time

from selenium.webdriver.common.by import By

from convert_date_format import convert_date_format
from find_name_position import find_name_position
from format_names import format_chinese_names
from mySavemoudle import MySaveData
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from re_match import re_match


class WIPO_Search:
    def __init__(self, key_word):
        """
        :param key_word:  传入要查询的信息
        """

        self.target_name = None
        self.key_word = key_word
        self.url_list = []
        self.request_url = 'https://patentscope2.wipo.int/search/zh/search.jsf'
        self.base_url = 'https://patentscope2.wipo.int/search/zh/'
        self.browser = webdriver.Chrome(service=Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"))

    def get_url(self, content):
        obj = re.compile(r'<div class="ps-patent-result--title">.*?<a href="(?P<href>.*?)" onclick=""', re.S)
        result = obj.finditer(content)

        for item in result:
            href = self.base_url + item.group('href')
            self.url_list.append(href)
        print(self.url_list)

    def start_selenium(self):

        self.browser.get(self.request_url)
        # 空出来给用户过验证码的时间 要是手速快可以缩短
        time.sleep(20)

        self.browser.find_element(By.ID, "simpleSearchForm:fpSearch:input").send_keys(self.key_word)
        self.browser.find_element(By.ID, "simpleSearchForm:fpSearch:buttons").click()

        ele_select = self.browser.find_element(By.ID, "resultListCommandsForm:perPage:input")

        Select(ele_select).select_by_value('200')
        # 空出来等待页面更新的时间
        time.sleep(10)

        # 获取查询总页数
        # 仍然有部分问题 待修改 先跳过
        # page_num = self.browser.find_element(By.CSS_SELECTOR, r"#resultListCommandsForm\3ApageNumber")
        # total_page = int(page_num.text.split(' / ')[-1]) + 1
        # 另一个思路 不记录总页数 只是单纯的翻页并记录信息 直到翻页键失效跳出循环

        # 这个是planB 需要人去看一下更新后的总页数再手动传参
        # 因为原本计划的那个截取分母获取总页数的方式不知道为什么失败了 所以改成手动的了（呜呜呜
        # 希望后来者改善
        total_pages = input('总页数：')
        print(total_pages)
        total_page = int(total_pages)

        html = self.browser.page_source

        self.get_url(html)

        for i in range(total_page):

            try:
                # 定位下一页按钮进行翻页
                next_page_link = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.js-paginator-next"))
                )

                # 点击“下一页”链接
                next_page_link.click()
                # 得到网页源代码
                # 等待跳转的响应时间 根据情况改 应该是有封装了等待功能的函数的 可惜我不会用 只能是最笨的方法了
                # WebDriverWait跟until函数混合使用应该能解决该问题
                time.sleep(2)
                html = self.browser.page_source

                self.get_url(html)
                i += 1
            except:
                i -= 1

    def parse_detail_url(self):
        # 解析详情网址
        for url in self.url_list:
            print(url)
            self.browser.get(url)
            # 因为打开界面有延迟 内容没加载完毕 所以需要time.sleep 根据网络情况自行更改 一般4-6之间基本就ok了
            #  WebDriverWait跟until函数混合使用应该能解决该问题
            time.sleep(4)
            html = self.browser.page_source

            # 解析每个详情页的数据
            self.parse_details(html, url)

    def parse_details(self, html, url):
        # 解析具体详情页面内容

        tb_header = ['专利局', '申请号', '申请日', '公布号', '公布日', '国际申请号', '国际申请日', '授权号', '授权日',
                     '公布类型', '国际专利分类', 'CPC', '申请人', '发明人', '第几发明人', '代理人', '优先权数据', '公布语言',
                     '申请语言', '标题', '摘要', '详情页网址',]
        tb_data = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                   None, None, None, None, None, url,]

        for field in tb_header:
            if field == '专利局':
                tb_data[0] = re_match(html, '专利局')
                continue

            if field == '申请号':
                tb_data[1] = re_match(html, '申请号')
                continue

            if field == '申请日':
                tb_data[2] = re_match(html, '申请日')
                tb_data[2] = convert_date_format(tb_data[2])
                continue

            if field == '公布号':
                tb_data[3] = re_match(html, '公布号')
                continue

            if field == '公布日':
                tb_data[4] = re_match(html, '公布日')
                tb_data[4] = convert_date_format(tb_data[4])
                continue

            if field == '国际申请号':
                tb_data[5] = re_match(html, '国际申请号')
                continue

            if field == '国际申请日':
                tb_data[6] = re_match(html, '国际申请日')
                tb_data[6] = convert_date_format(tb_data[6])
                continue

            if field == '授权号':
                tb_data[7] = re_match(html, '授权号')
                continue

            if field == '授权日':
                tb_data[8] = re_match(html, '授权日')
                tb_data[8] = convert_date_format(tb_data[8])
                continue

            if field == '公布类型':
                tb_data[9] = re_match(html, '公布类型')
                continue

            if field == '国际专利分类':
                tb_data[10] = re_match(html, '国际专利分类')
                continue

            if field == 'CPC':
                tb_data[11] = re_match(html, 'CPC')
                continue

            if field == '申请人':
                tb_data[12] = re_match(html, '申请人')
                continue

            if field == '发明人':
                tb_data[13] = re_match(html, '发明人')
                tb_data[13] = format_chinese_names(tb_data[13])
                # 标注出是第几发明人 如果没匹配到则对应的名字会返回-1
                # 返回-1一般有两种情况

                # 一种情况是因为是模糊匹配 其实匹配到了名字相似的人的专利 可以利用这个返回值发现模糊匹配错误的情况
                # 可以增加一个改进，即自动剔除所有返回-1的无关专利项目，但首先需要保证第二种情况不出现，期待后来者的改进

                # 另一种情况是因为前面网页资源没有加载完全 导致页面的所有元素都没有提取成功，跟空元素匹配最后返回-1
                # 这个情况可以通过增加time.sleep的时间来解决，或者用WebDriverWait跟until函数混合使用应该能解决该问题
                tb_data[14] = find_name_position(tb_data[13], self.target_name)
                continue

            if field == '代理人':
                tb_data[15] = re_match(html, '代理人')
                continue

            if field == '优先权数据':
                tb_data[16] = re_match(html, '优先权数据')
                continue

            if field == '公布语言':
                tb_data[17] = re_match(html, '公布语言')
                continue

            if field == '申请语言':
                tb_data[18] = re_match(html, '申请语言')
                continue

            if field == '标题':
                tb_data[19] = re_match(html, '标题')
                continue

            if field == '摘要':
                tb_data[20] = re_match(html, '摘要')
                continue

        print(tb_data)

        # 保存数据的方式 可以自己修改
        # MySaveData('专利数据', tb_data, tb_header).csv_save()
        MySaveData('专利数据', tb_data, tb_header).xlsx_save()

    def run(self):
        self.target_name = input('想要匹配的作者名字：')
        self.start_selenium()
        self.parse_detail_url()


if __name__ == '__main__':
    key_word = input('信息：')
    WIPO_Search(key_word).run()
