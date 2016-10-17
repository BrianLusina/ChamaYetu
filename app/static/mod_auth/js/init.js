(function($){
  $(function(){

    $('.button-collapse').sideNav();

    //trigger all modals
    $('.modal-trigger').leanModal();

    /*trigger register chama modal to register a new chama*/
    $("#register-user-btn").on("click", function(){
        /*close the register user modal*/
        $('.modal-trigger').closeModal();
        /*open the register chama modal*/
        $('.chama-modal-trigger').leanModal();
    });

    });
})(jQuery);
