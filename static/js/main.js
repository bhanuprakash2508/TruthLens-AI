document.addEventListener("DOMContentLoaded", function(){

    const form = document.querySelector("form");
    const button = document.querySelector("button");

    if(form){

        form.addEventListener("submit", function(){

            button.innerText = "Analyzing...";
            button.disabled = true;

        });

    }

});