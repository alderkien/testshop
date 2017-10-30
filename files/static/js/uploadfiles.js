
function init(){
	
    var imagesPreview = function(input, placeToInsertImagePreview) {
        if (input.files) {
            var filesAmount = input.files.length;
            for (i = 0; i < filesAmount; i++) {
                var reader = new FileReader();
                reader.onload = function(event) {
                    $(placeToInsertImagePreview).attr('src',event.target.result);
                }

                reader.readAsDataURL(input.files[i]);
            }
        }

    };

    $(document).on('change','.fileAjaxUpload',function(e){
        e.stopPropagation();
        $("#picpew"+this.id).remove();
        $(this).after('<img style="width: 50px; height: 50px;" id="picpew'+this.id+'"" src="">');
        imagesPreview(this, '#picpew'+this.id);
    });
}

$(document).ready(init());


