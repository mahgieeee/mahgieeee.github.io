window.onscroll = function() {scrollFunction()};

var x = window.matchMedia("(max-width: 700px)")
myFunction(x) // Call listener function at run time
x.addListener(myFunction) // Attach listener function on state changes


function scrollFunction() {
    if (x.matches){
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
            document.getElementById("logo").style.fontSize = "18px";
            } else {
            document.getElementById("topnav-container").style.padding = "40px 10px";
            document.getElementById("logo").style.fontSize = "28px";
    }
}

}