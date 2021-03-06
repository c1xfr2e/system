#!/usr/bin/env python3
# coding: utf-8

import pymongo


URI = "mongodb://localhost:27017"
DB = "hyle"

cli = pymongo.MongoClient(URI)[DB]

FundCompany = cli["fund_company"]
Fund = cli["fund"]
Stock = cli["stock"]
StockFundPosition = cli["stock_fund_position"]
FundCompanyPosition = cli["fund_company_position"]
FundCompanyPositionChange = cli["fund_company_position_change"]
