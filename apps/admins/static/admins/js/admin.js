$(document).ready(function(){

    // Admin login page
    $('.adlogout').fadeOut(2000)

    // Admin orders dashboard page
    $('#orders').fadeIn(800)

    // Admin products dashboard page
    $('#edit-modal').on('show.bs.modal', function(event){
        var link = $(event.relatedTarget)
        var prod = link.data('blah')
        $(this).find('.modal-title').text('Edit Product - ID ' + prod)
    })

    $('#delete-modal').on('show.bs.modal', function(event){
        var link = $(event.relatedTarget)
        var prod = link.data('blah2')
        $(this).find('.modal-title').text('Are you sure you want to delete product ' + prod +"?")
        $(this).find('#deleteprod').attr('action', '/admin/delete/' + prod)
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
            if (x == "8") $("a[page='after']").parent().addClass("disabled")
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
            if ($("a[page='8']").parent().hasClass('active')) $("a[page='after']").parent().addClass("disabled")
            else $("a[page='after']").parent().removeClass("disabled")
            if ($("a[page='1']").parent().hasClass('active')) $("a[page='before']").parent().addClass("disabled")
            else $("a[page='before']").parent().removeClass("disabled")
        }

        $.ajax({
            url: "/product/adminprodpaginate",
            data: {number: num},
            success: function(resp){
                $('#adminprods').html(resp)
            }
        })
    })

    $('#adminsearchp').on('submit', function(e){
        e.preventDefault()
    })

    $('#adminsearchp').keyup(function(){
        $('#pagenumbers').hide()
        $.ajax({
            method: "POST",
            url: "/product/adminprodsearch",
            data: $(this).serialize(),
            success: function(resp){
                $('#adminprods').html(resp)
            }
        })
    })

    $('#adminorderp').submit(function(e){
        e.preventDefault()
        $('#pagenumbers').hide()
        $.ajax({
            method: "POST",
            url: "/product/adminprodorder",
            data: $(this).serialize(),
            success: function(resp){
                $('#adminprods').html(resp)
            }
        })
    })

    $(".admindelete").fadeOut(1500)
    $(".adminadd").fadeOut(1500)

})