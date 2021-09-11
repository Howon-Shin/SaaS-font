const canvas = document.getElementById("jsCanvas");
const ctx = canvas.getContext("2d");

const CANVAS_SIZE = 400;

canvas.width = CANVAS_SIZE;
canvas.height = CANVAS_SIZE;

const INITIAL_COLOR = "black"
ctx.lineWidth = 10;

ctx.strokeStyle = INITIAL_COLOR;
ctx.fillStyle = INITIAL_COLOR;

let painting = false;
let filling = false;

let pushArray = new Array();
let doStep = -1;

function startPainting(event) {
    painting = true;
}

function stopPainting(event) {
    if (painting === true && filling === true) {  // 채우기 모드 용
        ctx.fill();
    }
    painting = false;
    push();
}

function onMouseMove(event) {
    const x = event.offsetX;
    const y = event.offsetY;
    if (!painting) {
        ctx.beginPath();
        ctx.moveTo(x, y);
    } else {
        ctx.lineTo(x, y);
        ctx.stroke();
    }
}

if (canvas) {
    canvas.addEventListener("mousemove", onMouseMove);
    canvas.addEventListener("mousedown", startPainting);
    canvas.addEventListener("mouseup", stopPainting);

    // 배경 흰색으로 깔기
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    ctx.fillStyle = "black";
    push();
}

// 붓 두께조절
const range = document.getElementById("jsRange");

function handleRangeChange(event) {
    const size = event.target.value;
    ctx.lineWidth = size;
}

if (range) {
    range.addEventListener("input", handleRangeChange);
};

// 채우기 or 칠하기 or 지우개 모드 변경
const mode_brush = document.getElementById("jsMode_brush");
const mode_fill = document.getElementById("jsMode_fill");
const mode_erase = document.getElementById("jsMode_erase");
const erase_all = document.getElementById("jsEraseAll");

function handleBrushClick() {
    filling = false;
    ctx.strokeStyle = 'black';
}
function handleFillClick() {
    filling = true;
    ctx.strokeStyle = 'black';
}
function handleEraseClick() { // 지우개는 clear가 아니라 흰색 브러쉬
    filling = false;
    ctx.strokeStyle = 'white';
}
function handleEraseAllClick() {
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    ctx.fillStyle = 'black';
    push();
}

if (mode_brush) {
    mode_brush.addEventListener("click", handleBrushClick);
}
if (mode_fill) {
    mode_fill.addEventListener("click", handleFillClick);
}
if (mode_erase) {
    mode_erase.addEventListener("click", handleEraseClick);
}
if (erase_all) {
    erase_all.addEventListener("click", handleEraseAllClick);
}

// 세이브 기능
$(document).ready(function(){
    $('#jsSave').click(function(){
        this.disabled = true;
        const data = canvas.toDataURL();
        const letter = document.getElementById('working').textContent;
        saveImage(data, letter, abling(this));

        // 중복클릭 방진데 잘안되는거 같음
        function abling(save_btn) {
            save_btn.disabled = false;
        }
    });
});

function saveImage(img, letter, complete_fn = null) {
    $.ajax({ // base64포멧으로 이미지 업로드
        type: 'POST',
        url: 'saveImg/',
        data: {data: img, letter: letter},
        success: function(result) {
            alert("업로드완료");
        },
        error: function(req, stat, e) {
            alert("에러발생");
        },
        complete: function() {
            if (complete_fn) complete_fn();
        }
    });
}

// 불러오기 기능
const load = document.getElementById("jsLoad");

function handleLoadClick() {
    let img = new Image();
    img.src = document.getElementById('working').textContent;
    load.disabled = true;
    // 캔버스 지우고 불러오기

    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    ctx.fillStyle = 'black';

    img.onload = function() {
        ctx.drawImage(img, 0, 0);
        //alert("이미지 로드");
    }
    push();
    load.disabled = false;
}

if (load) {
    load.addEventListener("click", handleLoadClick);
}

// 언두 리두 기능
const undo = document.getElementById('jsUndo');
const redo = document.getElementById('jsRedo');

function push() {
    doStep++;
    if (doStep < pushArray.length) { pushArray.length = doStep; }
    pushArray.push(canvas.toDataURL());
}

function undoClick() {
    if (doStep > 0) {
        doStep--;
        let canvasPic = new Image();
        canvasPic.src = pushArray[doStep];
        canvasPic.onload = function () { ctx.drawImage(canvasPic, 0, 0); }
    }
}

function redoClick() {
    if (doStep < pushArray.length - 1) {
        doStep++;
        let canvasPic = new Image();
        canvasPic.src = pushArray[doStep];
        canvasPic.onload = function () { ctx.drawImage(canvasPic, 0, 0); }
    }
}

if (undo) {
    undo.addEventListener("click", undoClick);
}
if (redo) {
    redo.addEventListener("click", redoClick);
}

// 드래그앤 드롭으로 파일 띄우기
function dragOver(e) {
    e.stopPropagation();
    e.preventDefault();
}

function uploadFiles(e) {
    e.stopPropagation();
    e.preventDefault();

    e.dataTransfer = e.dataTransfer;
    let files = e.target.files || e.dataTransfer.files;

    if (files.length > 1) {
        for (const file of files) {
            if (!file.type.match(/image.*/)) {
                alert(file.name + "은 이미지 파일이 아닙니다.");
                continue;
            }
            if (!file.name.match(/^\S\.\w*/)) {
                alert(file.name + ": 파일 이름은 한 글자여야 합니다.");
                continue;
            }

            const letter = file.name.slice(0, 1);
            createImgBase64(file, letter);
        }
        return;
    }

    if (files[0].type.match(/image.*/)) {
        const letter = document.getElementById('working').textContent;
        createImgBase64(files[0], letter);
    } else {
        alert('이미지가 아닙니다.');
        return;
    }

    function createImgBase64(file, letter) {
        createImageBitmap(file).then(function(img) {
            // saveImg로 보내기 위해 base64 데이터로 변환
            let cvs = document.createElement('CANVAS');
            let ctx_load = cvs.getContext('2d');
            cvs.height = img.height;
            cvs.width = img.width;
            ctx_load.drawImage(img, 0, 0);
            let dataURL = cvs.toDataURL();

            saveImage(dataURL, letter, handleLoadClick);

            push();
        });
    }
}

if (canvas) {
    canvas.addEventListener('dragover', dragOver);
    canvas.addEventListener('dragleave', dragOver);
    canvas.addEventListener('drop', uploadFiles);
}

handleLoadClick();
handleEraseAllClick();