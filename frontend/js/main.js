function uploadImage() {
    let input = document.getElementById("imageInput");
    let file = input.files[0];
    if (!file) {
        alert("Please select an image.");
        return;
    }
    let formData = new FormData();
    formData.append("image", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").innerHTML = data.message;
        })
        .catch(error => console.error("Error:", error));
}

function analyzeImage() {
    alert("Image analysis feature not implemented yet.");
}