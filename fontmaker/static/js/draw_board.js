const canvas = document.getElementById("jsCanvas");
const ctx = canvas.getContext("2d");

const CANVAS_SIZE = 400;

canvas.width = CANVAS_SIZE;
canvas.height = CANVAS_SIZE;

const INITIAL_COLOR = "#2c2c2c"
ctx.lineWidth = 10;

ctx.strokeStyle = INITIAL_COLOR;
ctx.fillStyle = INITIAL_COLOR;

let painting = false;
let filling = false;
let erasing = false;

function startPainting(event) {
    painting = true;
}

function stopPainting(event) {
    if (painting === true && filling === true) {  // 채우기 모드 용
        ctx.fill();
    }
    painting = false;
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
        if (erasing) {  // 지우개
            const eraserWidth = ctx.lineWidth;
            ctx.clearRect(x, y, eraserWidth, eraserWidth);
        } else {  // 브러쉬
            ctx.lineTo(x, y);
            ctx.stroke();
        }
    }
}

if (canvas) {
    canvas.addEventListener("mousemove", onMouseMove);
    canvas.addEventListener("mousedown", startPainting);
    canvas.addEventListener("mouseup", stopPainting);
    canvas.addEventListener("mouseleave", stopPainting);
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

// 채우기 or 칠하기 모드 변경
const mode = document.getElementById("jsMode");

function handleModeClick() {
    if (filling === false && erasing === false) {
        filling = true;
        mode.innerText = "지우개"
    } else if (filling === true && erasing === false) {
        filling = false;
        erasing = true;
        mode.innerText = "일반 브러쉬";
    } else {
        erasing = false;
        mode.innerText = "채우기 브러쉬";
    }
}

if (mode) {
    mode.addEventListener("click", handleModeClick)
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
}

if (load) {
    load.addEventListener("click", handleLoadClick);
}