let sequencial = 2
function AddInput(){
     num = sequencial++
     form =  `<div class="formulario"><div><label for="id${num}">Código do produto</label><input name="id${num}" type="text" id="id${num}" ></div><div><label for="quantity${num}">Quantidade</label><input name="quantity${num}" type="text" id="quantity${num}"/></div><div><label for="removal${num}">Motivo da remoção</label><input name="removal${num}" type="text" id="removal${num}" /></div></div>` 

     document.querySelector("#form").insertAdjacentHTML("afterbegin", form)
}