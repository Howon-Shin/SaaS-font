import { layer_popup } from "./project_popup.js";

// 프로젝트 삭제/탈퇴 기능
$(document).ready(function(){
    $('#proj-delete').click(function(){
        this.disabled = true;
        if (confirm("프로젝트를 삭제하시겠습니까?")) {
            deleteProject();
        }
        this.disabled = false;
    });

    $('#proj-exit').click(function(){
        this.disabled = true;
        if (confirm("프로젝트에서 나가시겠습니까?")) {
            exitProject();
        }
        this.disabled = false;
    });
});

function deleteProject() {
    $.ajax({
        type: 'POST',
        url: 'deleteProj/',
        success: function(result) {
            if (result == {'right': 'no'}) {
                alert("권한이 없습니다.");
            } else {
                alert("프로젝트 삭제 완료");
                location.href = "/"
            }
        },
        error: function(req, stat, e) {
            alert("에러발생");
        },
    });
}

function exitProject() {
    $.ajax({
        type: 'POST',
        url: 'exitProj/',
        success: function(result) {
            if (result == {'right': 'no'}) {
                alert("권한이 없습니다.");
            } else {
                alert("프로젝트 탈퇴 완료");
                console.log(result);
                if (result.error == 'noerror') {
                } else {
                    let successor = result.successor
                    if (successor) {
                        alert("프로젝트가 " + successor + "에게 양도되었습니다.");
                    } else {
                        alert("남은 인원이 없어 프로젝트가 삭제되었습니다.");
                    }
                }

                location.href = "/"
            }
        },
        error: function(req, stat, e) {
            alert("에러발생");
        },
    });
}

// 멤버 추가 및 관리
$(document).ready(function(){
    $('#member-invite').click(function(){
        let $href = $(this).attr('href');
        layer_popup($href, 2);
    });
    $('#member-manage').click(function(){
        let $href2 = $(this).attr('href');
        layer_popup($href2, 3);
    });

    $('#invite-btn').click(function(){
        this.disabled = true;
        let memberID = document.getElementById('name').value;
        if (confirm("해당 팀원을 초대하시겠습니까?")) {
            inviteMember(memberID);
        }
        this.disabled = false;
    });

    $('#manage-btn').click(function(){
        this.disabled = true;
        let memberID = document.getElementById('name2').value;
        let level = document.getElementById('level').value;
        if (confirm("해당 팀원의 권한을 변경하시겠습니까?")) {
            manageMember(memberID, level);
        }
        this.disabled = false;
    });

    $('#fire-btn').click(function(){
        this.disabled = true;
        let memberID = document.getElementById('name2').value;
        if (confirm("해당 팀원을 !!추방!!하시겠습니까?")) {
            fireMember(memberID);
        }
        this.disabled = false;
    });
});


function inviteMember(memberID) {
    $.ajax({
        type: 'POST',
        url: 'inviteMember/',
        data: {memberID: memberID},
        success: function(result) {
            if (result.error == 'noerror') {
                alert("초대 완료");
            } else if (result.error == 'nomember') {
                alert("잘못된 member ID 입니다.");
            } else if (result.error == 'selfinvite') {
                alert("본인입니다.");
            } else {
                alert("권한이 없습니다.");
            }
        },
        error: function(req, stat, e) {
            alert("에러발생");
        },
    });
}


function manageMember(memberID, level) {
    $.ajax({
        type: 'POST',
        url: 'manageMember/',
        data: {memberID: memberID, level: level},
        success: function(result) {
            if (result.error == 'noerror') {
                alert("변경 완료");
            } else if (result.error == 'samelevel') {
                alert("이미 해당 권한자입니다.");
            } else if (result.error == 'nolevel') {
                alert("설정 불가능한 권한입니다.");
            } else {
                alert("권한이 없습니다.");
            }
        },
        error: function(req, stat, e) {
            alert("에러발생");
        },
    });
}


function fireMember(memberID) {
    $.ajax({
        type: 'POST',
        url: 'fireMember/',
        data: {memberID: memberID},
        success: function(result) {
            if (result.error == 'noerror') {
                alert("추방 완료");
            } else if (result.error == 'nomember') {
                alert("잘못된 member ID 입니다.");
            } else {
                alert("권한이 없습니다.");
            }
        },
        error: function(req, stat, e) {
            alert("에러발생");
        },
    });
}