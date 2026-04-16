document.addEventListener('DOMContentLoaded', function() {
    var imageInput = document.getElementById('imageInput');
    var imagePreview = document.getElementById('imagePreview');
    var reconstructButton = document.getElementById('reconstructButton');
    var demoButton = document.getElementById('demoButton');
    var demoInput = document.getElementById('demoInput');
    var uploadButton = document.getElementById('uploadButton');
    var imagesPath

    // Lắng nghe sự kiện khi người dùng chọn hình ảnh
    imageInput.addEventListener('change', function(event) {
        var files = event.target.files; // Lấy danh sách các tệp đã chọn

        // Xóa bỏ các hình ảnh trước đó
        imagePreview.innerHTML = '';

        // Hiển thị nút "Reconstruct" sau khi người dùng đã chọn hình ảnh
        reconstructButton.style.display = files.length > 0 ? 'inline-block' : 'none';
        uploadButton.style.display = files.length > 0 ? 'inline' : 'none';
        // Duyệt qua từng tệp đã chọn và hiển thị hình ảnh
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            if (file.type.match('image.*')) {
                var reader = new FileReader();

                // Đọc và hiển thị hình ảnh
                reader.onload = function(e) {
                    var img = document.createElement('img');
                    img.src = e.target.result;
                    imagePreview.appendChild(img);
                };

                // Đọc dữ liệu của tệp
                reader.readAsDataURL(file);
            }
        }
    });    


    uploadButton.addEventListener('click', function(event) {
        event.preventDefault()
        uploadButton.style.display = 'none'
        var uploadForm = document.getElementById('uploadForm');
        var formData = new FormData(uploadForm);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Xử lý phản hồi từ máy chủ nếu cần
            imagesPath = data.message
            console.log(imagesPath);
        })
        .catch(error => {
            console.error('There was a problem with the upload:', error);
        });
    });

    reconstructButton.addEventListener('click', function() {
        // Tạo body của yêu cầu POST
        const requestBody = {
            path: imagesPath
        }
        // Tạo options cho fetch
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        };
        // Gửi yêu cầu POST đến localhost:7000/reconstruct
        fetch('http://localhost:7000/reconstruct', requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            // Xử lý phản hồi từ máy chủ nếu cần
        })
        .catch(error => {
            console.error('There was a problem with the request:', error);
        });
        console.log(requestBody)
        //window.location.href = 'loading'
    });
    


    demoInput.addEventListener('change', function(event) {
        var folderName = event.target.files[0].name;
        folderName = folderName.replace(/\.obj$/i, '');
        window.location.href = 'loading?file=' + encodeURIComponent(folderName);
    });

    demoButton.addEventListener('click', function() {
        demoInput.click();
    });
});
