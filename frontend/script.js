document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.getElementById("uploadBtn");
    const fileInput = document.getElementById("fileInput");
    const getResults = document.getElementById("getResults");

    uploadBtn.addEventListener("click", function () {
        const file = fileInput.files[0];
        if (!file) {
            uploadResult.textContent = "Please select a file first.";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        fetch("/analyze", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);

                // if (data.success) {
                //     const uploadResult = document.getElementById("uploadResult");
                //     imgCard.className = "bg-white p-4 rounded shadow";
                //     imgCard.innerHTML = `
                //         <img src="/images/${data.image}" alt="Image" class="w-full h-48 object-cover rounded">
                //         <p class="mt-2 text-center">Confidence: ${data.confidence}%</p>
                //     `;
                //     uploadResult.innerHTML = "";
                //     uploadResult.appendChild(imgCard);
                // } else {
                //     uploadResult.textContent = "Upload failed.";
                // }
            })
            .catch((error) => {
                console.error("Error uploading image:", error);
                uploadResult.textContent = "Upload failed.";
            });
    });

    getResults.addEventListener("click", function () {
        fetch("/results", {
            method: "GET",
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);

                const allResults = document.getElementById("allResults");
                allResults.innerHTML = "";
                data.images.forEach((image) => {
                    const imgCard = document.createElement("div");
                    imgCard.className = "bg-white p-4 rounded shadow";
                    imgCard.innerHTML = `
                        <img src="../backend/images/${image.url}" class="w-full h-48 object-cover rounded">
                        <p class="mt-2 text-center">Fire: ${image.fire}</p>
                        <p class="mt-2 text-center">Smoke: ${image.smoke}</p>
                        <p class="mt-2 text-center">Confidence: ${image.default}</p>
                    `;
                    allResults.appendChild(imgCard);
                });
            })
            .catch((error) => {
                console.error("Error fetching images:", error);
            });
    });
});
