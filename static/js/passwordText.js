const Password = () =>{
     const input = document.querySelectorAll("input")[1]
     const icon = document.querySelector("span")

     if(input.type === "password"){
          input.type = "text"
          icon.className = "fa-solid fa-eye"
     }else{
          input.type = "password"
          icon.className = "fa-solid fa-eye-slash"
     }
}