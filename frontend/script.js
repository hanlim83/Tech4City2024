document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.getElementById("uploadBtn");
    const fileInput = document.getElementById("fileInput");
    const getResults = document.getElementById("getResults");
    const uploadResult = document.getElementById("uploadResult");
    const loadingIcon = document.getElementById("loadingIcon");

    uploadBtn.addEventListener("click", function () {
        const file = fileInput.files[0];
        if (!file) {
            uploadResult.textContent = "Please select a file first.";
            return;
        }

        _analyzeFile(file);
    });

    getResults.addEventListener("click", function () {
        _fetchResults();
    });

    function _analyzeFile(file) {
        const formData = new FormData();
        formData.append("file", file);

        loadingIcon.classList.remove("hidden");
        uploadResult.textContent = "";

        fetch(`/analyze`, {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                loadingIcon.classList.add("hidden");

                if (data.downloadPath) {
                    uploadResult.textContent =
                        "Successfully uploaded and analyzed.";
                } else {
                    uploadResult.classList.remove("text-green-600");
                    uploadResult.classList.add("text-red-500");
                    uploadResult.textContent = "Upload failed.";
                    return;
                }

                const finalResult = document.getElementById("finalResult");
                finalResult.innerHTML = "";

                const imgCard = document.createElement("div");
                imgCard.className = "bg-white p-4 rounded shadow w-64 m-4";
                const fire =
                    data.fire !== null
                        ? `
                  <p class="mt-2 text-center text-red-500 font-bold">Fire Detected!</p>
                  <p class="mt-2 text-center">Fire: ${data.fire}</p>`
                        : "";
                const smoke =
                    data.smoke !== null
                        ? `
                  <p class="mt-2 text-center text-orange-400 font-bold">Smoke Detected!</p>
                  <p class="mt-2 text-center">Smoke: ${data.smoke}</p>`
                        : "";
                const undetected =
                    data.default !== null
                        ? `
                    <p class="mt-2 text-center text-green-500 font-bold">No fire or smoke detected</p>
                    <p class="mt-2 text-center">Undetected: ${data.default}</p>`
                        : "";

                imgCard.innerHTML = `
                        <img src="${data.downloadPath}" class="w-full h-48 object-contain rounded">
                        ${fire}
                        ${smoke}
                        ${undetected}
                    `;
                finalResult.appendChild(imgCard);
            })
            .catch((error) => {
                console.error("Error uploading video:", error);
                loadingIcon.classList.add("hidden");
                uploadResult.textContent = "Upload failed.";
            });
    }

    getResults.addEventListener("click", function () {
        fetch("/results", {
            method: "GET",
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);

                if (data.length == 0) {
                    alert("You have not uploaded any images.");
                } else {
                    const allResults = document.getElementById("allResults");
                    allResults.innerHTML = "";
                    data.forEach((image) => {
                        const imgCard = document.createElement("div");
                        imgCard.className =
                            "bg-white p-4 rounded shadow w-64 m-4";
                        const fire =
                            image.fire !== null
                                ? `
                  <p class="mt-2 text-center text-red-500 font-bold">Fire Detected!</p>
                  <p class="mt-2 text-center">Fire: ${image.fire}</p>`
                                : "";
                        const smoke =
                            image.smoke !== null
                                ? `
                  <p class="mt-2 text-center text-orange-400 font-bold">Smoke Detected!</p>
                  <p class="mt-2 text-center">Smoke: ${image.smoke}</p>`
                                : "";
                        const undetected =
                            image.default !== null
                                ? `
                    <p class="mt-2 text-center text-green-500 font-bold">No fire or smoke detected</p>
                    <p class="mt-2 text-center">Undetected: ${image.default}</p>`
                                : "";

                        imgCard.innerHTML = `
                        <img src="${image.downloadPath}" class="w-full h-48 object-contain rounded">
                        ${fire}
                        ${smoke}
                        ${undetected}
                    `;
                        allResults.appendChild(imgCard);
                    });
                }
            })
            .catch((error) => {
                console.error("Error fetching images:", error);
            });
    });
});
