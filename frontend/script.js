document.addEventListener('DOMContentLoaded', function() {
  const uploadBtn = document.getElementById('uploadBtn');
  const fileInput = document.getElementById('fileInput');
  const uploadResult = document.getElementById('uploadResult');
  const imageContainer = document.getElementById('imageContainer');
  const resultsTableBody = document.getElementById('resultsTableBody');

  uploadBtn.addEventListener('click', function() {
    const file = fileInput.files[0];
    if (!file) {
      uploadResult.textContent = 'Please select a file first.';
      return;
    }

    const formData = new FormData();
    formData.append('image', file);

    fetch('/process', {
      method : 'POST',
      body : formData,
    })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            uploadResult.innerHTML = `Upload successful! <a href="${
                data.url}" download>Download</a>`;
            loadImages();
          } else {
            uploadResult.textContent = 'Upload failed.';
          }
        })
        .catch(error => {
          console.error('Error uploading image:', error);
          uploadResult.textContent = 'Upload failed.';
        });
  });

  function loadImages() {
    fetch('/process')
        .then(response => response.json())
        .then(data => {
          imageContainer.innerHTML = '';
          data.images.forEach(image => {
            const imgCard = document.createElement('div');
            imgCard.className = 'bg-white p-4 rounded shadow';
            imgCard.innerHTML = `<img src="/images/${
                image}" alt="Image" class="w-full h-48 object-cover rounded">`;
            imageContainer.appendChild(imgCard);
          });
        })
        .catch(error => { console.error('Error fetching images:', error); });
  }

  function fetchResults() {
    fetch('/getAllResults')
        .then(response => response.json())
        .then(data => {
          resultsTableBody.innerHTML = '';
          data.forEach(result => {
            const row = document.createElement('tr');
            row.classList.add('border', 'border-gray-300');

            const idCell = document.createElement('td');
            idCell.classList.add('border', 'border-gray-300', 'px-4', 'py-2');
            idCell.textContent = result.id;
            row.appendChild(idCell);

            const filenameCell = document.createElement('td');
            filenameCell.classList.add('border', 'border-gray-300', 'px-4',
                                       'py-2');
            filenameCell.textContent = result.filename;
            row.appendChild(filenameCell);

            const resultCell = document.createElement('td');
            resultCell.classList.add('border', 'border-gray-300', 'px-4',
                                     'py-2');
            resultCell.textContent = result.result;
            row.appendChild(resultCell);

            resultsTableBody.appendChild(row);
          });
        })
        .catch(error => { console.error('Error fetching results:', error); });
  }

  loadImages();
  fetchResults();
});
