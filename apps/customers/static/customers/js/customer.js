$(document).ready(function(){
    // CodingDojo Ecommerce main page
    $('#mainpics').fadeIn(2000)
    $('.logout').fadeOut(2000)

    // figure out how to keep modal open if error messages show up (since page keeps redirecting to main)
    /* $('#login').submit(function(e){
        e.preventDefault()
        var str = $('#login').serialize()
        if (str){
            $('.error').show()
            console.log("no data")
        }
    }) */

    // Products dashboard
    $('#products').fadeIn(1500)
    $('#dashpics').fadeIn(2000)
    $('#user').fadeIn(2000)
    $('#pagenumbers').hide()

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

    $('#custsearch').keyup(function(){
        $(this).submit(function(e){
            e.preventDefault()
        })
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

})