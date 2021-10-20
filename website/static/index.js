function deleteNote(id){
    fetch("/delete-note", {
        method:"POST",
        body: JSON.stringify({id:id})
    }).then(res => window.location.href = "/")
    .catch(err => console.log(err))
}