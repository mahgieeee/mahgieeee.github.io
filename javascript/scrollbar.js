window.onscroll = function() {scrollFunction()};

var mq = window.matchMedia("only screen and (orientation:portrait) and (max-width: 280px)");

function scrollFunction(){
    if (!mq.matches){
        if (document.body.scrollTop > 10 || document.documentElement.scrollTop > 10) {
            document.getElementById("topnav-container").style.padding = "10px 10px";
            document.getElementById("logo").style.fontSize = "45px";
            } else {
            document.getElementById("topnav-container").style.padding = "40px 10px";
            document.getElementById("logo").style.fontSize = "58px";
            }
        }
    else{
        if (document.body.scrollTop > 10 || document.documentElement.scrollTop > 10) {
            document.getElementById("topnav-container").style.padding = "10px 10px";
            document.getElementById("logo").style.fontSize = "15px";
            } else {
            document.getElementById("topnav-container").style.padding = "20px 10px";
            document.getElementById("logo").style.fontSize = "18px";
            }
    }
}







/*
function scrollFunction() {
    if (document.body.scrollTop > 10 || document.documentElement.scrollTop > 10) {
    document.getElementById("topnav-container").style.padding = "10px 10px";
    document.getElementById("logo").style.fontSize = "45px";
    } else {
    document.getElementById("topnav-container").style.padding = "40px 10px";
    document.getElementById("logo").style.fontSize = "58px";
    }
}*/