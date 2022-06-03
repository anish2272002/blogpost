const pimg = document.querySelector("#accprofileimg");

document.querySelector("#id_profile_pic").addEventListener("change",()=>{
    console.log(this.files)
    const file = this.files[0]
    if(file){
        const reader = new FileReader();
        reader.addEventListener("load",()=>{
            console.log(this);
            pimg.setAttribute("src",this.result);
        })
        reader.readAsDataURL(file);
    }
})