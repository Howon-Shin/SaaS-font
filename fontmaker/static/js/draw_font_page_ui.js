function changeFont() {
    document.getElementById('preview-text').style.fontFamily = "굴림, arial";
}

function changeWorkingLetter() {
    let tc = document.getElementById('inputDefault').value;
    if (document.getElementById('guide-char').innerHTML != " ") document.getElementById('guide-char').innerHTML = tc[0];
    document.getElementById('inputDefault').value = tc[0];
    document.getElementById('working').textContent = tc[0];
    handleLoadClick();
}

function changeWorkingLetter_undone(character) {
    if (document.getElementById('guide-char').innerHTML != " ")
        document.getElementById('guide-char').innerHTML = character;
    document.getElementById('inputDefault').value = character;
    document.getElementById('working').textContent = character;
    handleLoadClick();
}

function guide_check(box) {
    if(box.checked)
        document.getElementById('guide-char').innerHTML = document.getElementById('working').textContent;
    else
        document.getElementById('guide-char').innerHTML = " ";
}