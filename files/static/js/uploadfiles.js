
function init(){
	
	$(document).on('change','.fileAjaxUpload',function(e){
        e.stopPropagation();
        var fileButton=$(this);
        var formData = new FormData();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        formData.append('csrfmiddlewaretoken',csrftoken);
        formData.append('img',fileButton.prop('files')[0])
        $.ajax({
            url: "",
            type: 'POST',
            data: formData,
            contentType:"multipart/form-data",
            datatype:'json',
            success: function (data) {
                $('#picprew_'+fileButton.attr('id')).remove();
                $(fileButton).val('');
                $(fileButton).after('<span id="picprew_'+fileButton.attr('id')+'"><input type=hidden name="'+fileButton.attr('name')+'" value="'+data['tmpfile']+'"><img style="width: 50px; height: 50px;" src="'+data['tmpfile']+'"></span>');
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


