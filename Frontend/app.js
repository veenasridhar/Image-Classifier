Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });

    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL; //This gets the base64 string  encoded URL of the image can be seen in inspect of the website 
    var server_url =  "http://127.0.0.1:5000/classify_image";

    $.post(server_url,
        {
            image_data:file.dataURL
        },
        function(data,status){
            console.log(data);
            
            /* This is a sample response got from the server
            
           0: {
                "class": "Haaland",
                "class_dictionary": {
                                    "Haaland": 0,
                                    "Ronaldo": 1,
                                    "Salah": 2,
                                    "Son": 3 },
                "class_probability": [33.51, 14.97, 44.17, 7.36]
}
            
            */

            //If the model fails to identify any face in the image
            
            if (!data || data.length == 0){
                $("#error").show();
                $("#resultHolder").hide();
                $("#divClassTable").hide();
            }

            // If there was a match found
            else{
                $("#error").hide();
                $("#resultHolder").show();
                matched_player = data[0].class_dictionary[data[0].class]
                console.log(matched_player)
                $("#resultHolder").html("The player is identified as "+ (data[0].class)+" with probability "+data[0].class_probability[matched_player]+"%.").html
                //let class_dictionary = data[0].class_dictionary

            }
        });

    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});
    
