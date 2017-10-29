
function init(){
	
	$(document).on('change','.fileAjaxUpload',function(e){
        e.stopPropagation();
        var fileButton=$(this);
        var formData = new FormData(fileButton);
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        formData.append('csrfmiddlewaretoken',csrftoken);
        $.ajax({
            url: "",
            type: 'POST',
            data: formData,
            contentType:"multipart/form-data",
            datatype:'json',
            success: function (data) {
                alert(data['tmpfile']);
                $(fileButton).after('<img style="width: 50px; height: 50px;" src="'+data['tmpfile']+'">');
            },
            error: function (data) {
                alert("Ошибка загрузки");
            },
            cache: false,
            contentType: false,
            processData: false
        });
	});

}

$(document).ready(init());


