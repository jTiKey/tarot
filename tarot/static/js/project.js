function ShowTimes() {
    var now = new Date();
    var hrs = checkTime(23-now.getUTCHours());
    var mins = checkTime(59-now.getUTCMinutes());
    var secs = checkTime(59-now.getUTCSeconds());
    var str = hrs+':'+mins+':'+secs;
    refresh(hrs, mins, secs);
    document.getElementById('countdownToMidnight').innerHTML = str;
}

function checkTime(i) {
    if (i < 10) {
        i = "0" + i
    }
    return i;
}

function refresh(hrs, mins, secs) {
    if (hrs == 0 && mins == 0 && secs == 0) {
        location.reload();
    }
}

setInterval('ShowTimes()',1000);
