function ConfirmDialog(qorigin, title, message, data) {
    $('<div></div>').appendTo('body')
                    .html('<div>'+message+'?</div>')
                    .dialog({
                        modal: true, title: title, zIndex: 10000, autoOpen: true,
                        width: 'auto', resizable: false,
                        buttons: {
                            Oui: function () {
                                Confirmresult(qorigin, true, data);
                                $(this).dialog("close");                               
                            },
                            Annuler: function () {                                                                
                                Confirmresult(qorigin, false, data);
                                $(this).dialog("close");
                            }
                        },
                        close: function (event, ui) {
                            $(this).remove();
                        }
                    });
};

function Confirmresult(qorigin, answer, data) {
    switch (qorigin){
        case "DelOwnRef":
            if (answer){
                $.ajax({
                    type: "POST",
                    url: '/CYL/DeleteReflection',
                    data: {'typeref': data[1] ,'idref': data[2] ,csrfmiddlewaretoken: csrftoken},
                    dataType: "json",
                    success: function(rs) {
                        alert(rs.message);
                        if (history.state==null) {
                            location.reload();
                        }
                        else{
                           GoAjax(history.state.url, history.state.slug, false);
                        }
                    },
                    error: function(rs, e) {
                        alert(rs.responseText);
                    }
                });
            }
        //case
    }
}

export{
    ConfirmDialog,
    Confirmresult,
};
