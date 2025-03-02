  function updateDateTime() {
    var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    var day = now.getDate();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();

    // 格式化日期和时间为两位数
    month = formatNumber(month);
    day = formatNumber(day);
    hour = formatNumber(hour);
    minute = formatNumber(minute);
    second = formatNumber(second);

    var dateString = year + '-' + month + '-' + day;
    var timeString = hour + ':' + minute + ':' + second;

    document.getElementById('datetime').innerHTML = "当前时间：" + dateString + " " + timeString;

    setTimeout(updateDateTime, 1000); // 每秒更新一次
}

// 添加一个函数来格式化数字，使其成为两位数的形式
function formatNumber(number) {
    return number < 10 ? '0' + number : number;
}

updateDateTime(); // 初始化调用
