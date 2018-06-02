//START GOOGLE ANALYTICS
(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = 'https://connect.facebook.net/ru_RU/sdk.js#xfbml=1&version=v3.0&appId=605044093212609&autoLogAppEvents=1';
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
//END GOOGLE ANALYTICS
//START language
$(document).ready(function () {
    var body = $('body');
    $('.lang-dropdown-click').click(function () {
        console.log('hover');
        var dropdown = $(this).find('.lang-dropdown');
        dropdown_func(dropdown)
    });

    var dropdown_func = function(event) {
        if (event.hasClass('d-block')) {
            event.parent().removeClass('active');
            event.removeClass('d-block');
        } else {
            event.parent().addClass('active');
            event.addClass('d-block');
        }
    };

    $('.change_language').on('click', function (e) {
        e.preventDefault();
        var form = $('.language_form');
        form.find('[name="language"]').val($(this).data('code'));
        form.submit();
    });

})//Language language