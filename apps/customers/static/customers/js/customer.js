$(document).ready(function(){
    // CodingDojo Ecommerce main page
    $('#mainpics').fadeIn(2000)
    $('.logout').fadeOut(2000)

    $('#login').submit(function(e){
        e.preventDefault()
        let errors = 0
        if($("#login_email").val() == ""){
            $('.lemail').remove()
            $('#login_email').before('<p class="error lemail">Please enter login email</p>')
            errors++
        }
        else $('.lemail').remove()
        if($("#login_password").val() == ""){
            $('.lpass').remove()
            $('#login_password').before('<p class="error lpass">Please enter login password</p>')
            errors++
        }
        else $('.lpass').remove()

        if (errors == 0) $("#login")[0].submit()
    })

    $('#registrar').submit(function(e){
        e.preventDefault()
        let errors = 0
        let email_regex = /^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-z]+$/
        if($("#first").val() == ""){
            $('.first').remove()
            $('#first').before('<p class="error first">Please enter your first name</p>')
            errors++
        }
        else if ($("#first").val().length < 3){
            $('.first').remove()
            $('#first').before('<p class="error first">First name must be at least 3 characters</p>')
            errors++
        }
        else $('.first').remove()
        if($("#last").val() == ""){
            $('.last').remove()
            $('#last').before('<p class="error last">Please enter your last name</p>')
            errors++
        }
        else if ($("#last").val().length < 3){
            $('.last').remove()
            $('#last').before('<p class="error last">Last name must be at least 3 characters</p>')
            errors++
        }
        else $('.last').remove()
        if($("#email").val() == ""){
            $('.email').remove()
            $('#email').before('<p class="error email">Please enter your email</p>')
            errors++
        }
        else if (!email_regex.test($("#email").val())){
            $('.email').remove()
            $('#email').before('<p class="error email">Email must be valid</p>')
            errors++
        }
        else $('.email').remove()
        if($("#password").val() == ""){
            $('.password').remove()
            $('#password').before('<p class="error password">Please enter your password</p>')
            errors++
        }
        else if ($("#password").val().length < 8){
            $('.password').remove()
            $('#password').before('<p class="error password">Password must be at least 8 characters</p>')
            errors++
        }
        else $('.password').remove()
        if($("#confirm").val() == ""){
            $('.confirm').remove()
            $('#confirm').before('<p class="error confirm">Please confirm your password</p>')
            errors++
        }
        else if ($("#password").val() != $("#confirm").val()){
            $('.confirm').remove()
            $('#confirm').before('<p class="error confirm">Passwords must match</p>')
            errors++
        }
        else $('.confirm').remove()

        if (errors == 0) $("#registrar")[0].submit()
    })

    // Products dashboard
    $('#products').fadeIn(1000)
    $('#dashpics').fadeIn(2800)
    $('#user').fadeIn(2000)
    $('#pagenumbers').hide()

    $('.placedorder').fadeOut(1500)

    $('.categories').click(function(){
        var cat = $(this).attr('cat')
        $('#pagenumbers').show()
        $.ajax({
            url: "/product/showprods",
            data: {category: cat},
            success: function(resp){
                $('#prodsection').html(resp)
            }
        })
    })

    $('.pages').click(function(){
        var page = $(this).attr("page")
        $('#pagenumbers').show()

        if (page == "after" && !$("a[page='after']").parent().hasClass("disabled")){
            $("a[page='before']").parent().removeClass("disabled")
            var aft = $(this).parent().siblings('.active').children().attr("page")
            var x = (parseInt(aft) + 1).toString()
            $(this).parent().siblings('.active').removeClass("active")
            $("a[page='"+x+"']").parent().addClass("active")
            if (x == "5") $("a[page='after']").parent().addClass("disabled")
        }
        if (page == "before" && !$("a[page='before']").parent().hasClass("disabled")){
            $("a[page='after']").parent().removeClass("disabled")
            var bef = $(this).parent().siblings('.active').children().attr("page")
            var x = (parseInt(bef) - 1).toString()
            $(this).parent().siblings('.active').removeClass("active")
            $("a[page='"+x+"']").parent().addClass("active")
            if (x == "1") $("a[page='before']").parent().addClass("disabled")
        }
        if (page == "after" || page == "before") num = $(this).parent().siblings('.active').children().attr("page")
        else{
            num = page
            $(this).parent().siblings('.active').removeClass("active")
            $(this).parent().addClass("active")
            if ($("a[page='5']").parent().hasClass('active')) $("a[page='after']").parent().addClass("disabled")
            else $("a[page='after']").parent().removeClass("disabled")
            if ($("a[page='1']").parent().hasClass('active')) $("a[page='before']").parent().addClass("disabled")
            else $("a[page='before']").parent().removeClass("disabled")
        }

        $.ajax({
            url: "/product/prodpaginate",
            data: {number: num},
            success: function(resp){
                $('#prodsection').html(resp)
            }
        })
    })

    $('#custsearch').submit(function(e){
        e.preventDefault();
    })

    $('#custsearch').keyup(function(){
        $('#pagenumbers').hide()
        $.ajax({
            method: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(resp){
                $('#prodsection').html(resp)
            }
        })
    })

    $('#sortby').submit(function(e){
        e.preventDefault()
        $('#pagenumbers').hide()
        $.ajax({
            method: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(resp){
                $('#prodsection').html(resp)
            }
        })
    })

    // One product
    $(".addedcart").fadeOut(1500);

    // Shopping cart
    $('#same').change(function(){
        if ($('#same').is(":checked")){
            $('#Bfname').val($('#Sfname').val())
            $('#Blname').val($('#Slname').val())
            $('#Baddress').val($('#Saddress').val())
            $('#Bcity').val($('#Scity').val())
            $('#Bstate').val($('#Sstate').val())
            $('#Bzip').val($('#Szip').val())
        }
    })

    $("#placeorder").submit(function(e){
        e.preventDefault()
        let errors = 0
        let card_regex = /^\d{4}-?\d{4}-?\d{4}-?\d{4}$/
        let code_regex = /^\d{3}$/
        let exp_regex = /^(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})$/
        if ($("#card").val() == ""){
            $('.card').remove()
            $('#card').before('<p class="error card">Please enter CC number</p>')
            errors++
        }
        else if (!card_regex.test($("#card").val())){
            $('.card').remove()
            $('#card').before('<p class="error card">Please enter a valid CC number</p>')
            errors++
        }
        else $('.card').remove()

        if ($("#code").val() == ""){
            $('.code').remove()
            $('#code').before('<p class="error code">Please enter security code</p>')
            errors++
        }
        else if (!code_regex.test($("#code").val())){
            $('.code').remove()
            $('#code').before('<p class="error code">Please enter a valid 3 digit code</p>')
            errors++
        }
        else $('.code').remove()

        if ($("#exp").val() == ""){
            $('.exp').remove()
            $('#exp').before('<p class="error exp">Please enter expiration date</p>')
            errors++
        }
        else if (!exp_regex.test($("#exp").val())){
            $('.exp').remove()
            $('#exp').before('<p class="error exp">Please enter a valid expiration date</p>')
            errors++
        }
        else $('.exp').remove()

        if (errors == 0) $("#placeorder")[0].submit()
    })

})