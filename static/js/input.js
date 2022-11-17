let begin = 1;
const AddField = () => {
  begin += 1;
  form = `<div id="field${begin}"><div><label for="id${begin}"></label><input name="id${begin}" required placeholder="Código do produto" type="text" id="id${begin}" ></div><div><label for="quantity${begin}"></label><input name="quantity${begin}"required placeholder="Quantidade" type="text" id="quantity${begin}"/></div><div><label for="removal${begin}"></label><input name="removal${begin}" required placeholder="Motivo da remoção" type="text" id="removal${begin}" /></div><button class="fa-solid fa-minus" type="button" onclick="RemoveField(${begin})"></button></div>`;

  document.querySelector("#field1").insertAdjacentHTML("afterend", form);
};

const RemoveField = (IdField) => {
  document.querySelector(`#field${IdField}`).remove();
};
