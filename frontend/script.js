document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.getElementById("uploadBtn");
    const fileInput = document.getElementById("fileInput");
    const uploadResult = document.getElementById("uploadResult");
    const imageContainer = document.getElementById("imageContainer");

    uploadBtn.addEventListener("click", function () {
        const file = fileInput.files[0];
        if (!file) {
            uploadResult.textContent = "Please select a file first.";
            return;
        }

        const formData = new FormData();
        formData.append("image", file);

        fetch("/analyse", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
            })
            .catch((error) => {
                console.error("Error uploading image:", error);
                uploadResult.textContent = "Upload failed.";
            });
    });

    function loadImages() {
        fetch("/get")
            .then((response) => response.json())
            .then((data) => {
                imageContainer.innerHTML = "";
                data.images.forEach((image) => {
                    const imgCard = document.createElement("div");
                    imgCard.className = "bg-white p-4 rounded shadow";
                    imgCard.innerHTML = `<img src="/images/${image}" alt="Image" class="w-full h-48 object-cover rounded">`;
                    imageContainer.appendChild(imgCard);
                });
            })
            .catch((error) => {
                console.error("Error fetching images:", error);
            });
    }

    loadImages();
});
