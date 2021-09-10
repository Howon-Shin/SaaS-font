import { layer_popup } from "./project_popup.js";

$(document).ready(function(){
    $('#undone-ascii').click(function(){
        $.ajax({
            type: 'GET',
            url: 'undone/',
            success: function(result) {
                let $href = $('#undone-ascii').attr('href');
                layer_popup($href, 1);

                let html = '';
                $.each(result.data, function(key, value){
                    html += "<a class='undone-chars' style='font-size:1.5em' onclick='changeWorkingLetter_undone(\""
                     + value + "\")'> " + value + " </a>";
                });

                $("#undone-chars-display").empty();
                $("#undone-chars-display").append(html);
            },
            error: function(e) {
                alert("에러발생");
            }
        });
    });
});