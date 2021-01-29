#!/usr/bin/env python3
# coding: utf-8

"""
    Query stock list from sse.com.cn

    返回数据格式：
    {
        "result": [
            {
                "COMPANY_CODE": "600000",
                "SECURITY_ABBR_A": "浦发银行",
                "SECURITY_ABBR_B": "-",
                "SECURITY_CODE_A": "600000",
                "SECURITY_CODE_B": "-",
                "totalShares": "2935208.04",
                "totalFlowShares": "2810376.39",
                "NUM": "1",
                "TYPE": "主板A股",
                "LISTING_DATE": "1999-11-10"
                "endDate": "2019-08-02",
            },
        ]
    }
"""

import logging
import pymongo
import requests
from collections import namedtuple
from datetime import datetime
from typing import List


stock = namedtuple(
    "stock",
    [
        "code",  # 6 位代码
        "name",  # 简称
        "list_date",  # 上市日期
    ],
)

STOCK_TYPE_MAIN = 1
STOCK_TYPE_KCB = 8


def _get_stock_list_by_page(page: int, stock_type) -> List[stock]:
    url = "http://query.sse.com.cn/security/stock/getStockListData.do"
    # 必须有 Referer， 否则调用非法
    headers = {
        "Referer": "http://www.sse.com.cn/assortment/stock/list/share/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) Chrome/75.0.3770.142 Safari/537.36",
    }
    params = {
        "isPagination": "true",
        "stockCode": "",
        "csrcCode": "",
        "areaName": "",
        "stockType": stock_type,  # 1: 主板A股  2: B股  8: 科创板
        "pageHelp.cacheSize": 1,
        "pageHelp.beginPage": page,  # 页数， 每次请求递增
        "pageHelp.pageSize": 50,  # 每次请求返回的股票数量， 最大 50
        "pageHelp.pageNo": 1,
    }
    resp = requests.get(url, headers=headers, params=params)
    if not resp.ok:
        logging.error("request failed: url=%s, response=%s", url, resp)
        resp.raise_for_status()
        return None
    result = resp.json()["result"]
    return [
        stock(
            code=r["SECURITY_CODE_A"].strip(),
            name=r["SECURITY_ABBR_A"].strip(),
            list_date=r["LISTING_DATE"],
        )
        for r in result
    ]


def get_stock_list(stock_type) -> List[stock]:
    """
    循环调用 _get_stock_list_by_page 获取全部股票列表
    """
    page = 1
    stock_list = []
    while True:
        p = _get_stock_list_by_page(page, stock_type)
        if not p:
            break
        page += 1
        stock_list.extend(p)
    return stock_list


def store_stock_list(mongo_col, stock_list):
    ops = [
        pymongo.UpdateOne(
            {"_id": stock.code},
            {
                "$set": {
                    "code": stock.code,
                    "name": stock.name,
                    "list_date": stock.list_date,
                    "update_time": datetime.now(),
                }
            },
            upsert=True,
        )
        for stock in stock_list
    ]
    mongo_col.bulk_write(ops)


if __name__ == "__main__":
    from shse import db

    # 主板
    main = get_stock_list(STOCK_TYPE_MAIN)
    store_stock_list(db.Stock, main)

    # 科创板
    kcb = get_stock_list(STOCK_TYPE_KCB)
    store_stock_list(db.Stock, kcb)
