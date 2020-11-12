$(document).ready(function(){
  $.ajaxSetup({ cache: false });

  var url = $('input#url').val();
  $('#login').html('<i class="icon-enter" style="padding-right: 10px;"></i>Connexion');

  $('#login').click(function(e){
    var email = $('.login-page').find("input[name=email]").val();
    var password = $('.login-page').find("input[name=password]").val();

    if(email == "" || password == ""){
      setTimeout(function(){
        $('.alert').addClass('alert-warning').html('Tu as oublié de remplir email ou mot de passe !').fadeIn();
        $('#login').html('<div class="icon-cross"></div>').addClass('error-input');

        setTimeout(function(){
          $('#login').html('<i class="icon-enter" style="padding-right: 10px;"></i>Connexion');
          $('#login-page button').removeClass('loading-animation').removeClass('error-input');
        }, 500)
      }, 1000)
    } else {
      $.ajax({
        url: url+"/root/homepage/login.php",
        method: 'POST',
        data: {
          login: 1,
          email: email,
          password: password
        },
        success: function (data) {
          setTimeout(function(){
            if(data.indexOf('Success') >= 0){
              setTimeout(function(){
                $('.alert').addClass('alert-success').html('Connexion...').fadeIn();
                $('#login').html('<div class="icon-checkmark"></div>').addClass('success-input');
                setTimeout(function(){ window.location.href = url; }, 1000)
              }, 500)
            } else {
              setTimeout(function(){
                $('.alert').addClass('alert-danger').html('Une erreur est survenue.').fadeIn();
                $('#login').html('<div class="icon-cross"></div>').addClass('error-input');

                setTimeout(function(){
                  $('#login').html('<i class="icon-enter" style="padding-right: 10px;"></i>Connexion');
                  $('#login-page button').removeClass('loading-animation').removeClass('error-input');
                }, 500)
              }, 500)
            }
          }, 600);
        },
        dataType:'text'
      });

    }
    e.preventDefault();
  });

});
