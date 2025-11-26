document.addEventListener("DOMContentLoaded", function () {
    const checkbox = document.querySelector("#id_aplica_direccion");
    const direccionInput = document.querySelector("#id_direccion");

    function actualizarDireccion() {
        if (!checkbox.checked) {
            direccionInput.value = "N/A";
        } else {
            // Solo limpiar si estaba en "N/A"
            if (direccionInput.value === "N/A") {
                direccionInput.value = "";
            }
        }
    }

    checkbox.addEventListener("change", actualizarDireccion);

    // Ejecutar al cargar la página
    actualizarDireccion();
});
