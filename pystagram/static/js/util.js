$(document).ready(function(){

		   $(window).scroll(function() {
      if ($(this).scrollTop() > 100) {
        $('#scroll-to-top').fadeIn();
      } else {
        $('#scroll-to-top').fadeOut();
      }
    });

	//스크롤 버튼 부드럽게 동작하기.
	 $('#scroll-to-top').click(function() {
      $('html, body').animate({scrollTop : 0},500);
      return false;
    });



	})


