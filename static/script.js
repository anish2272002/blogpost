var loadFile = function(event){
    var output = document.getElementById('accprofileimg');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
    URL.revokeObjectURL(output.src) // free memory
    }
};
const imginp = document.querySelector("#id_profile_pic");
if(imginp){
    imginp.addEventListener("change",loadFile);
}