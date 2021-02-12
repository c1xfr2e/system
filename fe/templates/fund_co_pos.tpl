<!DOCTYPE html>
<html>
<title>基金公司持仓</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<!-- <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> -->

<head>
  <script src="/static/js/fund_co_pos.js"></script>
  <style>
    .my-sidebar-item {
      font-size: 12px;
    }

  </style>
</head>

<body>
  <div class="w3-sidebar w3-bar-block w3-light-grey w3-card" style="width:170px">
    <h6 class="w3-bar-item w3-bottombar" style="margin-bottom:0">基金公司持仓</h6>
    {% for co in co_list %}
    <button class="w3-bar-item w3-button tablink my-sidebar-item"
            id="{{co["_id"]}}"
            onclick="openFundCompany(event, '{{co["_id"]}}')">{{co["co_name"]}}</button>
    {% endfor %}
  </div>

  <div style="margin-left:170px">

    <table class="w3-table w3-striped w3-hoverable w3-tiny">
      <thead>
        <tr class="w3-dark-grey">
          <th>股票</th>
          <th id="volume_in_float" onclick="sortColumn('volume_in_float')">流通比</th>
          <th id="total_percent" onclick="sortColumn('total_percent')">净值比</th>
          <th id="fund_count" onclick="sortColumn('fund_count')">基金数量</th>
        </tr>
      </thead>
      <tbody id="table_data">
      </tbody>
    </table>

  </div>

</body>
</html>