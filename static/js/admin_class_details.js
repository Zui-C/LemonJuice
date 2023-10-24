function load(data) {
    var data = JSON.parse(data)
    for (var i = 0; i < data.length; i++) {

        var c1 = document.createTextNode(data[i].c1);
        var c2 = document.createTextNode(data[i].c2);
        var c3 = document.createTextNode(data[i].c3);
        var c4 = document.createTextNode(data[i].c4+'%');
        var c5 = document.createTextNode(data[i].c5);
        var c6 = document.createTextNode(data[i].c6);
        var c7 = document.createTextNode(data[i].c7+'%');
        var c8 = document.createTextNode(data[i].c8+'%');
        var c9 = document.createTextNode(data[i].c9);
        var c10 = document.createTextNode(data[i].c10+'%');
        var c11 = document.createTextNode(data[i].c11+'%');
                var c13 = document.createTextNode(data[i].c13);

        //
        var c1a = document.createElement('a');
        c1a.href = "/admin/std_pg/"+data[i].c12+'/';
        c1a.target= "_blank";
        c1a.appendChild(c1);

        // 创建tr（创建行）
        var tr = document.createElement("tr");
        // 创建td，并赋于class和值（创建单元格，并输入值）

        var td1 = document.createElement("td");
        td1.className = "col1";
        td1.appendChild(c1a);
        var td2 = document.createElement("td");
        td2.className = "col2";
        td2.appendChild(c2);
        var td3 = document.createElement("td");
        td3.className = "col3";
        td3.appendChild(c3);
        var td4 = document.createElement("td");
        td4.className = "col4";
        td4.appendChild(c4);
        if(data[i].c4<8) td4.style.backgroundColor='red'
        var td5 = document.createElement("td");
        td5.className = "col5";
        td5.appendChild(c5);
        if(data[i].c5<5000) td5.style.backgroundColor='red'
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
        var td11 = document.createElement("td");
        td11.className = "col11";
        td11.appendChild(c11);
        var td13 = document.createElement("td");
        td13.className = "col13";
        td13.appendChild(c13);
        // 获取table1
        var table = document.getElementById("table1");
        // 将tr加入table中
        table.appendChild(tr);
        // 将td依次加入tr中
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td10);

        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        tr.appendChild(td6);
        tr.appendChild(td9);
        tr.appendChild(td11);

        tr.appendChild(td7);
        tr.appendChild(td8);

        tr.appendChild(td13);

    }


}
