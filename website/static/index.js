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
