//Date handling stuff
$('.date-analyze').click(function(){
    var text = $('.date-input').val();
    $('.date-analyzed').html('<center><img style="margin-top:30%" src="/img/ajax-loader.gif"/></center>');
    $.ajax({
        type: 'POST',
        url: '/date',
        data: {text: escape(text)},
        success: function(data){
            $('.date-analyzed').html(unescape(data.text));
        }
    });
});
