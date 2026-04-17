var express = require('express');
var router = express.Router();
var fs = require('fs');
var path = require('path');
const multer = require('multer');

const UPLOADS_TEMP = path.join(__dirname, '../uploads/temp');
const PROJECTS_DIR = path.join(__dirname, '../projects');

// Ensure base directories exist
fs.mkdirSync(UPLOADS_TEMP, { recursive: true });
fs.mkdirSync(PROJECTS_DIR, { recursive: true });

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, UPLOADS_TEMP);
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  }
});

const upload = multer({ storage: storage });

router.post('/upload', upload.array('files[]'), function(req, res, next) {
  const projectId = Date.now().toString();
  const projectPath = path.join(PROJECTS_DIR, projectId);
  const imagesFolderPath = path.join(projectPath, 'images');

  fs.mkdirSync(imagesFolderPath, { recursive: true });

  // Move files from temp to project images folder
  fs.readdirSync(UPLOADS_TEMP).forEach(file => {
    fs.renameSync(
      path.join(UPLOADS_TEMP, file),
      path.join(imagesFolderPath, file)
    );
  });

  res.json({ projectId });
});

/* GET home page. */
router.get('/', function(req, res, next) {
  fs.readFile(path.join(__dirname, '../public/html/index.html'), 'utf8', function(err, data) {
    if (err) return next(err);
    res.set('Content-Type', 'text/html');
    res.send(data);
  });
});

router.get('/modelview', function(req, res, next) {
  fs.readFile(path.join(__dirname, '../public/html/modelview.html'), 'utf8', function(err, data) {
    if (err) return next(err);
    res.set('Content-Type', 'text/html');
    res.send(data);
  });
});

router.get('/loading', function(req, res, next) {
  fs.readFile(path.join(__dirname, '../public/html/loading.html'), 'utf8', function(err, data) {
    if (err) return next(err);
    res.set('Content-Type', 'text/html');
    res.send(data);
  });
});

module.exports = router;
