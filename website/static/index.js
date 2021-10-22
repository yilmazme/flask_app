const questLength = document.getElementById("quest-length");
const answeredLength = document.getElementById("answered-length");
const rightLength = document.getElementById("right-length");
const result = document.getElementById("result");
const ratioDiv = document.getElementById("ratio");
const commentDiv = document.getElementById("comment");

questLength? questLength.innerHTML =sessionStorage.getItem("qLength") : null;
answeredLength? answeredLength.innerHTML = sessionStorage.getItem("aLength") : null;
rightLength? rightLength.innerHTML = sessionStorage.getItem("rLength"): null;


window.addEventListener("load",()=>{
  if(sessionStorage.getItem("qLength") != sessionStorage.getItem("aLength") || sessionStorage.getItem("aLength")==0){
    result.style.display = "none"
  }else{
    result.style.display = "block"
    let ratio = (sessionStorage.getItem("rLength") / sessionStorage.getItem("qLength"))*100
    if(ratio>=80){
      result.style.backgroundColor = "green"
      ratioDiv.innerHTML=ratio + "/100"
      commentDiv.innerHTML="O bir uzman, o mütevazı bir insan..."
    }
    else if(80>ratio && ratio>=60)
    {
      ratioDiv.innerHTML=ratio + "/100"
      commentDiv.innerHTML="Fena değil ama daha iyi olabilir, bunu sen de biliyorsun..."
    }
    else
    {
      result.style.backgroundColor = "red"
      ratioDiv.innerHTML=ratio + "/100"
      commentDiv.innerHTML="Bu sonuç sana yakışıyor mu?"
    }
  }
})

//result.innerHTML =  sessionStorage.getItem("rLength") / sessionStorage.getItem("qLength");

function makeChoice(questionId, choosenOp) {
  //alert(questionId, choosenOp)
  fetch("/make-choice", {
    method: "POST",
    body: JSON.stringify({ questionId: questionId, choosenOp: choosenOp }),
  })
    .then((res) => res.json())
    .then((data) => {
      let qDiv = document.getElementById(questionId);
      let choosenDiv = document.getElementById(choosenOp + questionId);

      if (data.res) {
        qDiv.style.backgroundColor = "green";
        choosenDiv.style.color = "white";
        sessionStorage.setItem(
          "rLength",
          JSON.stringify(JSON.parse(sessionStorage.getItem("rLength")) + 1)
        );
      } else {
        let correctDiv = document.getElementById(data.answer + questionId);
        choosenDiv.style.textDecoration = "underline";
        qDiv.style.backgroundColor = "red";
        correctDiv.style.color = "white";
      }
      getNextQuest();
      sessionStorage.setItem(
        "aLength",
        JSON.stringify(JSON.parse(sessionStorage.getItem("aLength")) + 1)
      );
    })
    .catch((err) => console.log(err));
}

function getNextQuest() {
  let idArray = JSON.parse(sessionStorage.getItem("idArray"));
  idArray.splice(0, 1);
  if (idArray.length == 0) {
    setTimeout(()=>{
      window.location.href = "/home";
    }, 1500)
  } else {
    sessionStorage.setItem("idArray", JSON.stringify(idArray));
    setTimeout(() => {
      window.location.href = "/questions/" + idArray[0];
    }, 1000);
  }
}

// in home html call this function for each category to get all question belong a category as json, not used for now
function callCategory(id) {
  sessionStorage.removeItem("idArray");
  let idArray = [];
  fetch("/get-set", {
    method: "POST",
    body: JSON.stringify({ id: id }),
  })
    .then((res) => res.json())
    .then((data) => {
      idArray = data.res.map((el) => el.id);
      sessionStorage.setItem("idArray", JSON.stringify(idArray));
      sessionStorage.setItem("qLength", JSON.stringify(idArray.length));
      sessionStorage.setItem("aLength", JSON.stringify(0));
      sessionStorage.setItem("rLength", JSON.stringify(0));
    })
    .catch((err) => console.log(err));

  window.location.href = "/home/" + id;
}

function deleteNote(id) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ id: id }),
  })
    .then((res) => (window.location.href = "/profile"))
    .catch((err) => console.log(err));
}

function deleteAccount(id) {
  let flag = confirm("Emin misiniz? ");

  if (flag) {
    fetch("/delete-account", {
      method: "POST",
      body: JSON.stringify({ id: id }),
    })
      .then((res) =>
        setTimeout(() => {
          window.location.href = "/home";
        }, 1000)
      )
      .catch((err) => console.log(err));
  }

  return;
}
