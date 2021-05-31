$(document).ready(function() {
$('.ajax-form').on('submit',function(e){

    $('.error-text').text('');
    $('.non-field-errors').text('');
    e.preventDefault();
    current_elem = $(this);
    submit_url = $(this).data('url');

    //var csrfmiddlewaretoken
    //var csrf = $(this).find('input[name="csrfmiddlewaretoken"]').val();
    //var dataString = "csrfmiddlewaretoken="+csrf;

    var formData = $(this).serializeArray();

    $.ajax({
        url: submit_url,
        type:'post',
        data:formData,
        success:(function( data ) {

            if (typeof(data) == "string") {
              data = JSON.parse(data)
            }
            else{
               console.log('data is not string');
            }

            if (data.errors){
                errors = data.errors
                console.log(errors);
                for (key in errors){
                   console.log('error key')
                    console.log(key);
                    if (key == "__all__"){
                        console.log('all errors');
                        $(document).find('.non-field-errors').text(errors[key]);
                    }
                    error_component=$(current_elem).contents().find("[name='"+key+"']").siblings(".error-text");

                    error_component.text("*"+errors[key]);
                    if (error_component.length){
                        console.log('no error-text found');
                    }
                    else{
                        console.log('error-text found');
                    }

                    // console.log(errors[key]);
                }


            }
            else{

                redirect_url = data.success_url;
                if (redirect_url){
                    console.log('redirect url found')
                    window.location.href = redirect_url
                    return false;
                }
                else{
                    console.log('redirect url not found');
                }

                 var success_message = data.message;
                 if (success_message){
                    $('.success-message').text(success_message)
                 }

            }
     }


     ),
      })

});

});

/* $(document).ready(function() {

  $(function() {
     $('.date-time').bootstrapMaterialDatePicker(
     { format : 'DD/MM/YYYY - HH:mm' }
     );

  });
});
*/

/*
$(document).ready(function() {

  $(function() {
     $('.date-input').bootstrapMaterialDatePicker(
     { format : 'DD/MM/YYYY',time:false }
     );

  });


});
*/