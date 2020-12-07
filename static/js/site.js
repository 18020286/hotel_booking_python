jQuery(function ($) {
    /**
	 * Site header scroll
	 */
    if ($(window).scrollTop() > 550) {
        $('.site-header').addClass('scroll');
        $('.site-mobile').addClass('scroll');
    }
    $(window).scroll(function () {
        if ($(this).scrollTop() > 550) {
            $('.site-header').addClass('scroll');
            $('.site-mobile').addClass('scroll');
        } else {
            $('.site-header').removeClass('scroll');
            $('.site-mobile').removeClass('scroll');
        }
    });
    $('.page-child').css({ 'padding-top': $('.site-header').outerHeight() });
    $(window).resize(function () {
        $('.page-child').css({ 'padding-top': $('.site-header').outerHeight() });
    });

    $('.site-scroll-down').on('click touchstart', function () {
        $('html, body').animate({
            scrollTop: $('.site-content').offset().top - $('.site-header').height()
        }, 600);
    });

    /**
	 * Site nav
	 */
    $('.aside-nav-toggler').on('click touchstart', function () {
        $('body').addClass('open-aside-nav').append('<div class="aside-overlay"></div>').css('overflow', 'hidden');
    });
    $('body').on('click touchstart', '.aside-nav-closer, .aside-overlay', function (e) {
        e.stopPropagation();
        $('body').removeClass('open-aside-nav').css('overflow', '');
        $('.aside-overlay').remove();
    });
    $('.aside-nav li.menu-item-has-children').on('click touchstart', function (e) {
        e.stopPropagation();
        $(this).siblings().children('.sub-menu').slideUp(300);
        $(this).toggleClass('active').children('.sub-menu').slideToggle(300);
    });
    $('.aside-nav li.menu-item-has-children > a').on('click touchstart', function (e) {
        e.stopPropagation();
    });

    /**
	 * Booking
	 */
    $('body').on('click', function () {
        $('#site-booking').collapse('hide');
    });
    $('.site-booking').on('click', function (e) {
        e.stopPropagation();
    });

    /**
	 * Site slider
	 */
    $('.home .site-slider').on('init', function () {
        $(this).find('.slick-slide').height($(window).height() - $('.site-mobile-bottom-bar').height());
    });
    $(window).resize(function () {
        $('.home .site-slider .slick-slide').height($(window).height() - $('.site-mobile-bottom-bar').height());
    });
    $('.site-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        fade: true,
        speed: 5000,
        autoplay: true,
        autoplaySpeed: 5000,
        dots: true,
        arrows: false
    });
    $('.site-video video').on('ended', function () {
        $('.site-slider').slick('slickGoTo', 0);
        $('.site-video').remove();
    });

    /**
	 * Home intro content
	 */
    $('.home-intro-content .toggle').on('click touchstart', function () {
        $('.home-intro-content .hidden').slideToggle(300);
        $(this).toggleClass('open');
    });

    /**
	 * Single room facilities
	 */
    $srf = $('.single-room-facilities');
    if ($srf.length > 0) {
        if ($srf.height() > parseInt($('html').css('font-size')) * 7.75) {
            $srf.after('<div class="srf-toggle"><a href="javascript:void()">More info</a></div>');
        }
    }
    $('body').on('click touchstart', '.srf-toggle a', function () {
        $srf.toggleClass('open');
    });

    /**
	 * Fancybox
	 */
    $('[data-fancybox]').fancybox({
        youtube: {
            showinfo: 0
        },
        thumbs: {
            autoStart: true
        },
        afterShow: function (instance, current) {
            $('.tab-pane.active .col-gallery').each(function () {
                if ($(this).find('.gallery').data('thumb-type') == 'video') {
                    $('.fancybox-thumbs li').eq($(this).index()).append('<i class="fa fa-play play"></i>');
                }
            });
        }
    });

    /**
	 * Bootstrap
	 */
    $('[data-toggle="popover"]').popover();
    $('[data-toggle*="tooltip"]').tooltip();

    /**
	 * Single room gallery
	 */
    $('.single-room-gallery').owlCarousel({
        margin: 10,
        responsiveClass: true,
        nav: true,
        navText: ['<i class="ion-ios-arrow-left"></i>', '<i class="ion-ios-arrow-right"></i>'],
        responsive: {
            0: {
                items: 1,
            },
            576: {
                items: 2,
            },
            992: {
                items: 3,
            }
        }
    });
    /**
	 * Single Offer
	 */
    $('.single-offer').owlCarousel({
        margin: 10,
        responsiveClass: true,
        nav: true,
        navText: ['<i class="ion-ios-arrow-left"></i>', '<i class="ion-ios-arrow-right"></i>'],
        responsive: {
            0: {
                items: 1,
            },
            576: {
                items: 2,
            },
            992: {
                items: 2,
            }
        }
    });
    /**
	 * Login facebook
	 */
    if (window.location.hash && window.location.hash == '#_=_') {
        window.location.hash = '#logged-in';
    }

    /**
	 * Form book
	 */
    if (window.location.hash.indexOf('#modal-') !== -1) {
        $modal = $(window.location.hash);
        $modal.modal('show');
    }
    $('[href^="#modal-"]').on('click touchstart', function () {
        $modal = $($(this).attr('href'));
        $modal.modal('show');
        $modal.find('.modal-title').text($(this).text());
        $modal.find('[name="book"]').val($(this).text());
        $modal.find('[name="page"]').val($(this).data('page'));
        $modal.find('.alert').remove();
    });

    $('.form-customer, .form-contact, .form-login, .form-signup, .form-forgot-password, .form-change-password').on('submit', function (e) {
        e.preventDefault();
        var $this = $(this);
        $this.find('.btn').append('<i class="ion-loop spin icon"></i>');
        $this.find('.alert').remove();
        $.ajax({
            type: 'POST',
            url: ajax.ajax_url,
            data: $this.serialize(),
            success: function (data, textStatus, jqXHR) {
                $this.find('.btn').find('.icon').remove();
                if (data.status == false) {
                    $this.append('<div class="alert alert-danger">' + data.message + '</div>');
                } else {
                    $this.find('.form-control').val('');
                    $this.append('<div class="alert alert-success">' + data.message + '</div>');
                    if ($this.hasClass('form-login')) window.location.href = '/';
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseText);
            }
        });
    });
    $('.form-book').on('submit', function (e) {
        e.preventDefault();
        var $this = $(this);
        $this.find('.btn').append('<i class="ion-loop spin icon"></i>');
        $this.find('.alert').remove();
        if (checkOfferInput($("#offername").val(), $("#offerphone").val(), $("#offeremail").val(), $("#offerdate").val(), $("#offerpeople").val()) == true) {
            $.ajax({
                type: "POST",
                url: "/Ajax/AjaxBookSpecial.ashx",
                data: { 'name': $("#offername").val(), 'phone': $("#offerphone").val(), 'email': $("#offeremail").val(), 'date': $("#offerdate").val(), 'people': $("#offerpeople").val(), 'message': $("#offermessage").val(), 'page': $("#offerid").val() },
                success: function (data) {
                    $this.find('.btn').find('.icon').remove();
                    if (data == "ok") {
                        $this.find('.form-control').val('');
                        $this.append('<div class="alert alert-success">Your information has been submitted successfully. We will get back to you within 12 hours!</div>');
                        if ($this.hasClass('form-login')) window.location.href = '/';
                    } else {
                        $this.append('<div class="alert alert-danger">Error!</div>');
                    }
                }
            });
        } else {
            $this.append('<div class="alert alert-danger">Error!</div>');
        }
    });

    function checkOfferInput(_name, _phone, _email, _date, _people) {
        var ok = true
        if (_name == "") {
            $("#msoffername")[0].innerHTML = "Required Fields";
            ok = false;
        }
        else { $("#msoffername")[0].innerHTML = null; }
        if (_phone == "") {
            $("#msofferphone")[0].innerHTML = "Required Fields";
            ok = false;
        }
        else { $("#msofferphone")[0].innerHTML = null; }
        if (_email == "") {
            $("#msofferemail")[0].innerHTML = "Required Fields";
            ok = false;
        }
        else {
            $("#msofferemail")[0].innerHTML = null;
            var emailRegexStr = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
            var isvalid = emailRegexStr.test(_email);
            if (!isvalid) {
                $("#msofferemail")[0].innerHTML = "Invalid email address!";
                ok = false;
            }
        }
        if (_date == "") {
            $("#msofferdate")[0].innerHTML = "Required Fields";
            ok = false;
        }
        else { $("#msofferdate")[0].innerHTML = null; }
        if (_people == "") {
            $("#msofferpeople")[0].innerHTML = "Required Fields";
            ok = false;
        }
        else { $("#msofferpeople")[0].innerHTML = null; }
        //if (_message == "") {
        //    $("#msoffermessage")[0].innerHTML = "Required Fields";
        //    ok = false;
        //}
        //else { $("#msoffermessage")[0].innerHTML = null; }
        return ok;
    }
    function checknull(value) //tạo function
    {
        var _value = $("#" + value).val()
        if (_value == "") {
            $("#ms" + value)[0].innerHTML = "Required Fields";
        }
        else $("#ms" + value)[0].innerHTML = "";
    }
    function checkPolicynull(agreeToTerms) //tạo function
    {
        var _value = document.getElementsByName(agreeToTerms);
        if (_value[0].checked == true) {
            $("#mesg")[0].innerHTML = "";
        }
    }
    function checkEmailnull() //tạo function
    {
        var _email = $("#email").val()
        if (_email == "") {
            $("#msemail")[0].innerHTML = "Required Fields";
        }
        else {
            var emailRegexStr = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
            var isvalid = emailRegexStr.test(_email);
            if (!isvalid) {
                $("#msemail")[0].innerHTML = "Invalid email address!";
            }
            else $("#msemail")[0].innerHTML = "";
        }
    }
    /**
	 * Form comment
	 */
    $formComment = $('.form-comment');
    $formComment.on('submit', function (e) {
        e.preventDefault();
        var $this = $(this);
        $this.find('.btn').append('<i class="ion-loop spin icon"></i>');
        $.ajax({
            type: 'POST',
            url: ajax.ajax_url,
            data: $this.serialize(),
            success: function (data, textStatus, jqXHR) {
                $this.find('.btn').find('.icon').remove();
                if (data.status == false) {
                    $this.append('<div class="alert alert-danger">' + data.message + '</div>');
                } else {
                    $this.find('.form-control').val('');
                    $this.append('<div class="alert alert-success">' + data.message + '</div>');
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    });
    $('.comment .reply').on('click touchstart', function () {
        $formComment.find('input[name="parent"]').remove();
        $formComment.prepend('<input type="hidden" name="parent" value="' + $(this).data('parent') + '"/>');
        $('html, body').animate({
            scrollTop: $formComment.offset().top
        }, 600);
    });
    /**
	 * Open chat
	 */

});