function deleteNote(id) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ id: id }),
  })
    .then((res) => (window.location.href = "/"))
    .catch((err) => console.log(err));
}

function deleteAccount(id) {
  let flag = confirm("Emin misiniz? ");

  if (flag) {
    fetch("/delete-account", {
      method: "POST",
      body: JSON.stringify({ id: id }),
    })
      .then((res) => (setTimeout(()=>{
        window.location.href = "/home"
      }, 1000)))
      .catch((err) => console.log(err));
  }

  return;
}

function makeChoice(questionId, choosenOp){
  //alert(questionId, choosenOp)
  fetch("/make-choice", {
    method: "POST",
    body: JSON.stringify({ questionId: questionId, choosenOp: choosenOp }),
  })
    .then((res) => res.json())
    .then((data)=> {
      console.log(data)
      let qDiv = document.getElementById(questionId)
      let choosenDiv = document.getElementById(choosenOp+questionId)
      
      if(data.res){    
        qDiv.style.backgroundColor = "green";
        choosenDiv.style.color = "white";
      }
      else{
        let correctDiv = document.getElementById(data.answer+questionId)
        choosenDiv.style.textDecoration = "underline"
        qDiv.style.backgroundColor = "red";
        correctDiv.style.color = "white"
      }
    })
    .catch((err) => console.log(err));
}


// in home html call this function for each category to get all question belong a category as json, not used for now
// function callCategory(id){
//   fetch("/get-set", {
//     method: "POST",
//     body: JSON.stringify({ id: id }),
//   })
//     .then((res) => res.json())
//     .then((data)=> console.log(data))
//     .catch((err) => console.log(err));
// }