
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
                $(fileButton).after('<span id="picprew_'+fileButton.attr('id')+'"><img style="width: 50px; height: 50px;" src="'+data['path']+data['tmpfile']+'"></span>');
                $('#'+fileButton.attr('id')+'_str').val(data['tmpfile']);
            },
            error: function (data) {
                alert("Ошибка загрузки");
            },
            cache: false,
            contentType: false,
            processData: false
        });
	});
    
    $(document).on('click','#add_more',function() {
        var form_idx = $('#id_pics-TOTAL_FORMS').val();
        $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_pics-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });
}

$(document).ready(init());


