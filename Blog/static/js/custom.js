clicked = true;
    $(document).ready(function(){
        $(".share-btn").click(function(){
            if(clicked){
                $(".social-links").css('right', '-70px');
                $( ".share-btn" ).addClass( "hide-links" );
                $( ".share-btn" ).removeClass( "show-links" );
                clicked  = false;
            } else {
                $(".social-links").css('right', '0px');
                $( ".share-btn" ).addClass( "show-links" );
                $( ".share-btn" ).removeClass( "hide-links" );
                clicked  = true;
            }   
        });
    });