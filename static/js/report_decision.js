function load(data) {
    var data = JSON.parse(data)


    for (var i = 0; i < data.length; i++) {

        var c1 = document.createTextNode(data[i].c1);
        var c2 = document.createTextNode(data[i].c2);
        var c3 = document.createTextNode(data[i].c3);
        var c4 = document.createTextNode(data[i].c4);
        var c5 = document.createTextNode(data[i].c5);
        var c6 = document.createTextNode(data[i].c6);
        var c7 = document.createTextNode(data[i].c7);
        var c8 = document.createTextNode(data[i].c8);
        var c9 = document.createTextNode(data[i].c9);
        var c10 = document.createTextNode(data[i].c10);



        // 创建tr（创建行）
        var tr = document.createElement("tr");
        // 创建td，并赋于class和值（创建单元格，并输入值）
        var td1 = document.createElement("td");
        td1.className = "col1";
        td1.appendChild(c1);
        var td2 = document.createElement("td");
        td2.className = "col2";
        td2.appendChild(c2);
        var td3 = document.createElement("td");
        td3.className = "col3";
        td3.appendChild(c3);
        var td4 = document.createElement("td");
        td4.className = "col4";
        td4.appendChild(c4);
        var td5 = document.createElement("td");
        td5.className = "col5";
        td5.appendChild(c5);
        var td6 = document.createElement("td");
        td6.className = "col6";
        td6.appendChild(c6);
        var td7 = document.createElement("td");
        td7.className = "col7";
        td7.appendChild(c7);
        var td8 = document.createElement("td");
        td8.className = "col8";
        td8.appendChild(c8);
        var td9 = document.createElement("td");
        td9.className = "col9";
        td9.appendChild(c9);
        var td10 = document.createElement("td");
        td10.className = "col10";
        td10.appendChild(c10);


        // 获取table1
        var table = document.getElementById("table1");
        // 将tr加入table中
        table.appendChild(tr);
        // 将td依次加入tr中
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        tr.appendChild(td6);
        tr.appendChild(td7);
        tr.appendChild(td8);
        tr.appendChild(td9);
        tr.appendChild(td10);


    }
    // 改变当前共多少条数
    // 获取table有多少行
    var num = table.rows.length - 2;
    // 将行数写入
    var rowsNumber = document.getElementById("rowsNum");
    rowsNumber.innerHTML = "共 " + num + " 条";


    // 获取当前页面
    var page = document.getElementById("pno").innerText;
    page = parseInt(page);

    // 超过该页面显示数量的数据，不显示
    for (var i = (page * 10) + 2; i < num + 2; i++) {
        table.rows[i].style.display = "none";
    }

}


// 下一页
function next() {
    // 获取table1
    var table = document.getElementById("table1");
    var num = table.rows.length - 2;

    // 获取当前页面
    var page = document.getElementById("pno").innerText;
    page = parseInt(page);

    // 总页数
    var pageSum = Math.ceil((num) / 10);

    // 如果下一页小于总页数，则跳转到下一页，否则报出提示
    if (page < pageSum) {
        page = page + 1;
        document.getElementById("pno").innerText = page;
        for (var i = ((page - 2) * 10) + 2; i < ((page - 1) * 10) + 2; i++) {
            table.rows[i].style.display = "none";
        }
        for (var i = ((page - 1) * 10) + 2; i < (page * 10) + 2; i++) {
            table.rows[i].style.display = "table-row";
        }
    } else {
        window.alert("该页为最后一页，无法前往下一页！")
    }
}

// 上一页
function last() {
    // 获取table1
    var table = document.getElementById("table1");
    var num = table.rows.length - 2;

    // 获取当前页面
    var page = document.getElementById("pno").innerText;
    page = parseInt(page);

    // 如果是首页，则报出提示，否则跳转到上一页
    if (page > 1) {
        document.getElementById("pno").innerText = page - 1;
        for (var i = ((page - 2) * 10) + 2; i < ((page - 1) * 10) + 2; i++) {
            table.rows[i].style.display = "table-row";
        }
        for (var i = ((page - 1) * 10) + 2; i < (page * 10) + 2; i++) {
            table.rows[i].style.display = "none";
        }
    } else {
        window.alert("该页为首页，无法前往上一页！")
    }
}

function gopage() {
    // 获取table1
    var table = document.getElementById("table1");
    var num = table.rows.length - 2;

    // 获取跳转页面
    var page = document.getElementById("gopg").value;
    page = parseInt(page);


    // 总页数
    var pageSum = Math.ceil((num) / 10);

    if (page < pageSum) {
        for (var i = ((page - 1) * 10) + 2; i < (page * 10) + 2; i++) {
            table.rows[i].style.display = "table-row";
        }
        for (var i = 2; i < ((page - 1) * 10) + 2; i++) {
            table.rows[i].style.display = "none";
        }
        for (var i = (page * 10) + 2; i < num + 2; i++) {
            table.rows[i].style.display = "none";
        }
        document.getElementById("pno").innerText = page;
    }
    if (page == pageSum) {
        for (var i = ((page - 1) * 10) + 2; i < num + 2; i++) {
            table.rows[i].style.display = "table-row";
        }
        for (var i = 2; i < ((page - 1) * 10) + 2; i++) {
            table.rows[i].style.display = "none";
        }
        document.getElementById("pno").innerText = page;
    }
    if (page > pageSum) {
        window.alert("您输入的页码超出总页码，请重新输入！")
    }
}