/*
  app.js - Script de la ventana de confirmación para eliminar
  ------------------------------------------------------------
  En base.html hay un solo modal de Bootstrap (#modalEliminar) que
  comparten todos los listados. Cada botón de eliminar de las tablas
  tiene dos atributos:
    data-url    -> la ruta que borra el registro (ej: /duenos/3/eliminar)
    data-nombre -> el texto que se muestra en la pregunta

  Cuando el modal se va a abrir, leo esos atributos del botón que se
  presionó y los pongo en el formulario del modal. Así el registro solo
  se borra si el usuario confirma con el botón "Eliminar".
*/
document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("modalEliminar");
  if (!modal) return;

  // "show.bs.modal" es el evento que lanza Bootstrap justo antes de mostrar el modal
  modal.addEventListener("show.bs.modal", function (evento) {
    const boton = evento.relatedTarget; // el botón de eliminar que se presionó
    document.getElementById("formEliminar").action = boton.getAttribute("data-url");
    document.getElementById("nombreEliminar").textContent = boton.getAttribute("data-nombre");
  });
});
