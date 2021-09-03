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
        const data = canvas.toDataURL();
        const letter=document.getElementById('working').textContent;

        $.ajax({ // base64포멧으로 이미지 업로드
            type: 'POST',
            url: 'saveImg/',
            data: {data: data, letter: letter},
            success: function(result) {
                alert("업로드완료");
            },
            error: function(e) {
                alert("에러발생");
            }
        });
    });
});

// 불러오기 기능
const load = document.getElementById("jsLoad");

function handleLoadClick() {
    let img = new Image();
    img.src = document.getElementById('working').textContent;
    // 캔버스 지우고 불러오기
    ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    img.onload = function() {
        ctx.drawImage(img, 0, 0);
        alert("이미지 로드");
    }
    push();
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