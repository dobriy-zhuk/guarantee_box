$('form').submit(function () {
        event.preventDefault();
        let content_type = ($("input[name=content_type]").val());

           console.log($(this).serialize());

        //c plus plus compiler
        if(content_type === 'c_plus_plus'){
            let my_code = $.trim($("#my_code").val());
            if(my_code !== ""){

                let myVar = JSON.stringify({compiler: "gcc-head", "code": my_code, "options": "warning,gnu++1y", "compiler-option-raw": "-Dx=hogefuga\n-O3" });
                jQuery.ajax({
                    url:     "https://wandbox.org/api/compile.json",
                    type:     "POST",
                    dataType: "json",
                    data: myVar,
                    compiler:"gcc-head",
                    success: function(response) { //Если все нормально

                        $('#compilation-result').html(response.program_message);
                        var answer = document.getElementById("answer").getAttribute("data-value");
                        if (response.program_message === answer){
                            $('#result_id').html("Правильно!");



                            $.ajax({
                            type: "POST",
                            url: "http://127.0.0.1:8000/students/api/0/set-student-module-done/",
                            contentType: 'application/json; charset=utf-8',
                            processData: false,
                            data: JSON.stringify($(this).serialize()),
                            success: function (data) {
                                console.log(data);
                            },
                            error: function(e, x, r) {
                                console.log(e);
                            }
                          });


                        }
                        else {
                            $('#result_id').html("Подумай еще раз!");
                        }

                        },
                    error: function(response) { //Если ошибка
                        console.log("Error compile");
                    }
                });
            }
        }
    });
