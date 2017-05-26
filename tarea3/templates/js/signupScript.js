/**
 * Created by Ale (aka the merciful god) on 25-05-2017.
 */

function crearFormulario() {
    var bloques = parseInt(document.getElementById("bloques").value);
    var idRegion = "regiones" + bloques;
    var idComuna = "comunas" + bloques;
    var titulo = "<p>Título de Fotografía</p><input type=" + "text" + " name=" + "titulo[]" + " size=" + 30 + " maxlength=" + 50 + "><br>";
    var archivo = "<p>Archivo</p><input type=" + "file" + " name=" + "archivo[]" + " accept=" + "image/*" + "><br>";
    var etiquetas = "<p>Etiquetas</p><input type=" + "text" + " name=" + "etiqueta[]" + " size=" + 50 + " maxlength=" + 200 + "><br>";
    var regiones = "<p>Region</p><select id=" + "'" + idRegion + "'" + " name=" + "regiones[]" + " onchange=" + "getComunas(" + "'" + idRegion + "'" + "," + "'" + idComuna + "'" + ")" + "></select>";
    var comuna = "<p>Comuna</p><select id=" + "'" + idComuna + "'" + " name=" + "comunas[]" + "></select>";
    var separador = "<br><br>-----------------------------------------------------------------------------------<br><br>" + "-----------------------------------------------------------------------------------<br>";
    document.getElementById('formularioS').innerHTML += titulo;
    document.getElementById('formularioS').innerHTML += archivo;
    document.getElementById('formularioS').innerHTML += etiquetas;
    document.getElementById('formularioS').innerHTML += regiones;
    document.getElementById('formularioS').innerHTML += comuna;
    document.getElementById('formularioS').innerHTML += separador;
    selectRegiones(idRegion);
}
