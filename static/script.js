var loadFile = function(event){
    var output = document.getElementById('accprofileimg');
    if(event.target.files[0]){
        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
        };
    }
};
const imginp = document.querySelector("#id_profile_pic");
if(imginp){
    imginp.addEventListener("change",loadFile);
}

var loadblogFile = function(event){
    var output = document.getElementById('blogimg');
    if(event.target.files[0]){
        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
        };
    }
};
const blogimginp = document.querySelector("#id_image");
if(blogimginp){
    blogimginp.addEventListener("change",loadblogFile);
}