#conding=utf-8
"""
author:liqq
应用：获取菏泽市政府市长邮箱的数据，存到数据库，最终放到享TV
时间:2019-11-25
采用面向过程方式
"""
import requests as rq
from lxml import etree
import json
import pymysql
def getList():
	url = "http://www.heze.gov.cn/jact/front/dataproxy_mailpublist.do?startrecord=1&endrecord=66&perpage=19&groupSize=3"
	headers={
		"Accept":"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
		"Accept-Language":"zh-CN,zh;q=0.9",
		"Content-type":"application/x-www-form-urlencoded; charset=UTF-8",
		"Cookie":"_pubk=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFZrWF7IJ38IsT6eAXU0kY4NcTJoH%2BMk3BMi1u%0ABpal%2BDVxzf7ohU24YDG9%2BHcOVe%2BZgOwu4WnxSj9Hp3FufLIetX27mZqurzQ0GiuduZidVxsMcRnR%0ANwU9zVgOIsET9%2BKRsN%2FVw7qgk4I4xw%2B6TqESxwA1dbkCYzJCJ4LlBPhSwwIDAQAB%0A; JSESSIONID=0EBC62C430B5857F1C07AAA9FB3A13AC; zh_choose_62=s; wondersLog_sdywtb_sdk=%7B%22persistedTime%22%3A1574665689735%2C%22updatedTime%22%3A1574666123506%2C%22sessionStartTime%22%3A1574665691167%2C%22sessionReferrer%22%3A%22http%3A%2F%2Fwww.heze.gov.cn%2Fart%2F2019%2F9%2F23%2Fart_11713_303.html%22%2C%22deviceId%22%3A%224051f70ff4581aa340b20aa5b3706140-6834%22%2C%22LASTEVENT%22%3A%7B%22eventId%22%3A%22wondersLog_pv%22%2C%22time%22%3A1574666123505%7D%2C%22sessionUuid%22%3A5425258669618124%2C%22costTime%22%3A%7B%22wondersLog_unload%22%3A1574666123506%7D%7D",
		"Host":"www.heze.gov.cn",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
	}
	data={
		"sysid":"84",
		"datadetailid":"",
		"dicvalue":"",
		"mailnumber":"",
		"querycode":"",
		"groupid":"",
		"mailstate":"",
		"starttime":"",
		"endtime":"",
		"keyword":"",
		"orderfield":"1"

	}
	res=rq.post(url=url,data=data,headers=headers).content.decode("utf-8")
	data=res.split("dataStore = ")[1].rstrip(";")
	#print(data)
	#print(json.loads(data,strict=False)[0:50])
	for tr in json.loads(data,strict=False)[0:50]:
		data_dic={}
		tr_html=etree.HTML(tr)
		data_dic["question_number"]=tr_html.xpath("//tr/td[1]/text()")[0]
		data_dic["question_title"]=tr_html.xpath("//tr/td[2]/a/text()")[0]
		data_dic["question_url"]=tr_html.xpath("//tr/td[2]/a/@href")[0]
		data_dic["question_end"]=tr_html.xpath("//tr/td[3]/text()")[0]
		#data_dic["time"]=tr_html.xpath("//tr/td[4]/text()")[0]
		data_dic["question_clickNum"]=tr_html.xpath("//tr/td[5]/text()")[0]
		#print(data_dic)
		data_dic["question_content"],data_dic["question_time"],data_dic["response_content"],data_dic["response_time"],data_dic["response_department"]=getContent(data_dic["question_url"])
		#with open("data.txt","w") as f:
		#	f.write(data)
		#print(data_dic)
		insertData(data_dic)
def getContent(url):
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
	res=rq.get(url='http://www.heze.gov.cn/jact/front/'+url,headers=headers).content.decode("utf-8")
	res_html=etree.HTML(res)
	#//div[@class="jact_box_font"]//table//tr//td//span[@class="contentspan"]
	question_content=res_html.xpath('//div[@class="jact_box_font"]//table//tr[3]/td[2]/span/text()')[0]
	question_time=res_html.xpath('//div[@class="jact_box_font"]//table//tr[6]/td[4]/span/text()')[0]
	response_content=res_html.xpath('string(//div[@style="padding-bottom:15px;"]/table//tr[3]/td[2]/span)')
	response_time=res_html.xpath('//div[@style="padding-bottom:15px;"]/table//tr[4]/td[4]/span/text()')[0]
	response_department=res_html.xpath('//div[@style="padding-bottom:15px;"]/table//tr[4]/td[2]/span/a/text()')[0]
	#print(question_content+"==="+question_time+"===="+response_content+"===="+response_time+"==="+response_department)
	#print(question_content)
	return question_content,question_time,response_content,response_time,response_department
def insertData(dic):
	selectSql="select * from Mayor_mail where question_number='%s'"%(dic["question_number"])
	db=pymysql.connect("172.17.1.8","emspapp","emspapp","spider_db")
	cursor=db.cursor()
	cursor.execute(selectSql)
	if(cursor.rowcount!=0):
		print("编号为%s的问题已经存在，无需存储"%(dic["question_number"]))
	else:
		print("即将存储编号为%s的问题内容\n"%(dic["question_number"]))
		insertSql="insert into Mayor_mail(question_number,question_title,question_url,question_end,question_clickNum,question_content,question_time,response_content,\
		response_time,response_department) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(dic["question_number"],dic["question_title"],\
			dic["question_url"],dic["question_end"],dic["question_clickNum"],dic["question_content"],dic["question_time"],\
			dic["response_content"],dic["response_time"],dic["response_department"])
		cursor.execute(insertSql)
		db.commit()
		print("【新内容提醒】问题编号为%s的问题内容已经存到数据库"%(dic["question_number"]))
		cursor.close()

if __name__ == '__main__':
	getList()
