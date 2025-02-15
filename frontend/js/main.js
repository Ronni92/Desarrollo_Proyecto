function uploadImage() {
    let input = document.getElementById("imageInput");
    let file = input.files[0];

    if (!file) {
        alert("Por favor, selecciona una imagen.");
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
            document.getElementById("result").innerHTML = "Imagen cargada correctamente.";
        })
        .catch(error => console.error("Error:", error));
}

function analyzeImage() {
    // Simulación de datos
    let sampleData = [
        { hora: "08:00 AM", evento: "Clase de Matemáticas" },
        { hora: "10:00 AM", evento: "Reunión de Proyecto" },
        { hora: "12:30 PM", evento: "Almuerzo" },
        { hora: "03:00 PM", evento: "Estudio de Física" }
    ];

    let tableBody = document.querySelector("#scheduleTable tbody");
    tableBody.innerHTML = ""; // Limpiar tabla antes de agregar datos

    sampleData.forEach(item => {
        let row = `<tr><td>${item.hora}</td><td>${item.evento}</td></tr>`;
        tableBody.innerHTML += row;
    });

    document.getElementById("result").innerHTML = "Análisis completado.";
}
