// Buscamos los elementos de la pantalla que vamos a utilizar.
const boton = document.getElementById("comprobar-servidor");
const resultado = document.getElementById("resultado-servidor");

// Ejecutamos esta función cuando el usuario presiona el botón.
boton.addEventListener("click", async () => {
    boton.disabled = true;
    resultado.textContent = "Comprobando conexión…";

    try {
        // Pedimos datos a Python y esperamos su respuesta.
        const respuesta = await fetch("/api/estado", {
            cache: "no-store"
        });

        // Una respuesta HTTP de error también debe informarse.
        if (!respuesta.ok) {
            throw new Error("El servidor devolvió un error.");
        }

        // Convertimos el JSON recibido en un objeto de JavaScript.
        const datos = await respuesta.json();

        // Mostramos el mensaje como texto en la pantalla.
        resultado.textContent = datos.mensaje;
    } catch (error) {
        // Por ejemplo, si el servidor está apagado.
        resultado.textContent =
            "No se pudo comprobar el servidor. Revisá que esté encendido.";
    } finally {
        // Permitimos realizar otra comprobación.
        boton.disabled = false;
    }
});