var express = require('express');
var router = express.Router();
var fs = require('fs');
var path = require('path');
const multer = require('multer');

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'public/images/temp');
  },
  filename: function (req, file, cb) {
      // Tên tập tin sau khi tải lên
      cb(null, file.originalname);
  }
});

function generateRandomFolderName() {
  const currentDate = new Date();
  return currentDate.getTime().toString(); // Sử dụng thời gian hiện tại làm tên thư mục ngẫu nhiên
}

// Khởi tạo middleware multer với cài đặt lưu trữ
const upload = multer({ storage: storage });

// Phần xử lý tải lên ảnh
router.post('/upload', upload.array('files[]'), function(req, res, next) {
  const tempFolderPath = path.join(__dirname, '../public/images/temp');
  const finalFolderPath = path.join(__dirname, '../public/images', generateRandomFolderName());

  // Tạo thư mục cuối cùng với tên ngẫu nhiên
  fs.mkdirSync(finalFolderPath, { recursive: true });

  const imagesFolderPath = path.join(finalFolderPath, 'images');
  fs.mkdirSync(imagesFolderPath);

  // Di chuyển tất cả các tệp từ thư mục tạm thời vào thư mục cuối cùng
  fs.readdirSync(tempFolderPath).forEach(file => {
      const oldPath = path.join(tempFolderPath, file);
      const newPath = path.join(imagesFolderPath, file);
      fs.renameSync(oldPath, newPath);
  });
  // Trả về phản hồi dưới dạng JSON cho client
  res.json({ message: finalFolderPath });
});

/* GET home page. */
router.get('/', function(req, res, next) {
  fs.readFile(__dirname + '/../public/html/index.html', 'utf8', function(err, data) {
    if (err) {
      return next(err);
    }
    res.set('Content-Type', 'text/html');
    res.send(data);
  });
});

router.get('/modelview', function(req, res, next) {
  fs.readFile(path.join(__dirname, '../public/html/modelview.html'), 'utf8', function(err, data) {
    if (err) {
      return next(err);
    }
    res.set('Content-Type', 'text/html');
    res.send(data);
  });
});

router.get('/loading', function(req, res, next) {
  fs.readFile(path.join(__dirname, '../public/html/loading.html'), 'utf8', function(err, data) {
    if (err) {
      return next(err);
    }
    res.set('Content-Type', 'text/html');
    res.send(data);
  });
});

module.exports = router;
