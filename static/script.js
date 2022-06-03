const accfile = document.querySelector("#id_profile_pic");
const pimg = document.querySelector("#accprofileimg");

accfile.addEventListener("change",()=>{
    const file = this.files[0];
    if(file){
        const reader = new FileReader();
        reader.addEventListener("load",()=>{
            console.log(this);
            pimg.setAttribute("src",this.result);
        })
        reader.readAsDataURL(file);
    }
})