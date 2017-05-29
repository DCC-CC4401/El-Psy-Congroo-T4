/**
 * Created by Ale (aka the merciful god) on 25-05-2017.
 */

function crearFormulario() {
    var tipo = document.getElementById('tipo').value;
	document.getElementById('formasDePago').innerHTML="";
	document.getElementById('divHoraIni').innerHTML="";
	document.getElementById('divHoraFin').innerHTML="";

   if(tipo==2 || tipo== 3){
       //formas de pago
        var HTMLformasDePago = 'Seleccione sus formas de pago:'+
									'<p>'+
									'<input type="checkbox" class="filled-in" id="filled-in-box" name="formaDePago0" value="0"/>'+
									'<label for="filled-in-box">Efectivo</label>'+
									'</p>'+
									'<p>'+
									'<input type="checkbox" class="filled-in" id="filled-in-box2" name="formaDePago1" value="1"/>'+
									'<label for="filled-in-box2">Tarjeta de Crédito</label>'+
									'</p>'+
									'<p>'+
									'<input type="checkbox" class="filled-in" id="filled-in-box3" name="formaDePago2" value="2"/>'+
									'<label for="filled-in-box3">Tarjeta de Débito</label>'+
									'</p>'+
									'<p>'+
									'<input type="checkbox" class="filled-in" id="filled-in-box4" name="formaDePago3" value="3"/>'+
									'<label for="filled-in-box4">Tarjeta Junaeb</label>'+
									'</p>'+
									'</div>';
        document.getElementById('formasDePago').innerHTML=HTMLformasDePago;}


    if(tipo==2){
        var HTMLhoraIni='<i class="material-icons prefix">alarm</i>'+
								  '<input name="horaIni" id="icon_prefix" type="date" class="validate">'+
								  '<label for="icon_prefix">Hora inicial</label>';

        var HTMLhoraFin='<i class="material-icons prefix">alarm</i>'+
								   '<input name="horaFin" id="icon_telephone" type="date" class="validate">'+
                                   '<label for="icon_telephone">Hora final</label>';

        document.getElementById('divHoraIni').innerHTML=HTMLhoraIni;
        document.getElementById('divHoraFin').innerHTML=HTMLhoraFin;}

}
