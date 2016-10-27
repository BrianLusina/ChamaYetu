$('.toggle').on('click', function() {
  $('.auth_container').stop().addClass('active');
});

$('.close').on('click', function() {
  $('.auth_container').stop().removeClass('active');
});