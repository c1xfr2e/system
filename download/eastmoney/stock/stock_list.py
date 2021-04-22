#!/usr/bin/env python3
# coding: utf-8

"""
    get 沪深股票列表
    数据保存到 mongodb 的 stock collection
"""

import requests

from typing import Dict, List


def get_stock_total(session):
    """ get 沪深股票总数 """

    url = "http://3.push2.eastmoney.com/api/qt/clist/get"
    headers = {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)",
        "Accept": "*/*",
        "Referer": "http://quote.eastmoney.com/",
    }
    params = {
        "pn": 1,
        "pz": 1,
        "po": "1",
        "np": "1",
        "fltt": "2",
        "invt": "2",
        "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
    }
    resp = session.get(url, headers=headers, params=params)
    return resp.json()["data"]["total"]


def get_stock_list_by_page(session, page_number, page_size) -> List[Dict]:
    """
    分页 get 沪深股票列表

    Args:
        page_number: 页号 (首页为 1)
        page_size:   页大小

    Returns:
        股票列表, 带基本信息, 见 samples/stock_list.json
    """

    url = "http://3.push2.eastmoney.com/api/qt/clist/get"
    headers = {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)",
        "Accept": "*/*",
        "Referer": "http://quote.eastmoney.com/",
    }
    params = {
        "pn": page_number,
        "pz": page_size,
        "po": "1",
        "np": "1",
        "fltt": "2",
        "invt": "2",
        "fid": "f20",  # 按市值排序
        "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
        "fields": "f2,f3,f4,f5,f6,f7,f8,f12,f13,f14,f20,f21,f38,f39,f37,f23,f114,f9,f26",
    }
    resp = session.get(url, headers=headers, params=params)
    return resp.json()["data"]["diff"]


def _parse_fields(data):
    return {
        "code": data["f12"],
        "name": data["f14"],
        "price": data["f2"],
        "change": data["f3"],
        "volume": data["f5"],
        "amount": data["f6"],
        "amplitude": data["f7"],
        "turnover": data["f8"],
        "market": "sh" if data["f13"] == 1 else "sz",
        "total_value": data["f20"],
        "float_value": data["f21"],
        "total_shares": data["f38"],
        "float_shares": data["f39"],
        "roe": data["f37"],
        "pb": data["f23"],
        "pe_lyr": data["f114"],
        "pe_forecast": data["f9"],
        "list_date": data["f26"],
    }


def get_stock_list() -> List[Dict]:
    sess = requests.Session()
    stock_list = []
    total = get_stock_total(sess)
    page_no = 1
    page_size = 500
    while page_no <= total / page_size:
        data = get_stock_list_by_page(sess, page_no, page_size)
        page_no += 1
        stock_list.extend([_parse_fields(d) for d in data])
    return stock_list


if __name__ == "__main__":
    sess = requests.Session()
    print(get_stock_list_by_page(sess, 1, 10))
