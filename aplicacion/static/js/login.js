function validar() {
    let correo = document.getElementById("idcorreo").value;
    let pass = document.getElementById("contraseña").value;
    if (correo == ""){
        document.getElementById("msjCorreo").className = "text-danger"
        document.getElementById("msjCorreo").innerHTML = "Ingresa su Correo";
    }else{
        document.getElementById("msjCorreo").innerHTML="";
    }

    if (pass == ""){
        document.getElementById("msjClave").className = "text-danger"
        document.getElementById("msjClave").innerHTML = "Ingresa su contraseña";
    }else{
        document.getElementById("msjClave").innerHTML="";
    }
    

    let submitBtn = document.getElementById('submitBtn');
    if (correo !== '' && pass !== '') {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}