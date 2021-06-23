var bar = document.getElementById('bar');
var errorlabel = document.getElementById('error');
var btn = document.getElementById('submit')
bar.addEventListener('blur' , except);
function except() {
    bar.value = bar.value.trim();
    var content = bar.value;
    if(content.length == 0){
        return 0;
    }
    var count = (content.match(/ /g) || []).length;
    if (count != 0){
        errorlabel.innerHTML = 'wrong link!' ;
        btn.classList.add("disable");
        return 0;
    }
    var dot = (content.match(/\./g) || []).length;
    console.log(dot);
    if(dot == 0){
        errorlabel.innerHTML = 'wrong link!' ;
        btn.classList.add("disable");
        return 0;
    }
    btn.classList.toggle("disable", false);
    errorlabel.innerHTML = '' ;
}