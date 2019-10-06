window.onscroll = function() {scrollFunction()};
                
function scrollFunction() {
    if (document.body.scrollTop > 10 || document.documentElement.scrollTop > 10) {
    document.getElementById("topnav-container").style.padding = "10px 10px";
    document.getElementById("logo").style.fontSize = "45px";
    } else {
    document.getElementById("topnav-container").style.padding = "40px 10px";
    document.getElementById("logo").style.fontSize = "58px";
    }
}