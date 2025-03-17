document.addEventListener('DOMContentLoaded', function() {
    var progressBar = document.querySelector('.loading-bar');

    // Lấy tham số file từ URL hiện tại
    var urlParams = new URLSearchParams(window.location.search);
    var fileParam = urlParams.get('file');

    // Giả định rằng loading đạt 100% sau 3 giây
    setTimeout(function() {
        // Chuyển hướng sang trang /modelview với tham số file
        setTimeout(function() {
            window.location.href = '/modelview?file=' + encodeURIComponent(fileParam);
        }, 200); // Delay 1 giây trước khi chuyển hướng
    }, 3000); // Giả định thời gian loading là 3 giây
});
