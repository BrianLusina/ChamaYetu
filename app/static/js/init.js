(function($){
  $(function(){

    $('.button-collapse').sideNav();

    //trigger all modals
    $('.modal-trigger').leanModal();

  // Materialize.toast(message, displayLength, className, completeCallback);
  Materialize.toast('I am a toast!', 4000) // 4000 is the duration of the toast


  }); // end of document ready
})(jQuery); // end of jQuery name space