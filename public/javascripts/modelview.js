// Tạo một scene
var scene = new THREE.Scene();
scene.background = new THREE.Color(0x888888);

// Create lighting
var light = new THREE.PointLight(0xffffff, 1.5); 
light.position.set(-5, 10, 20);
light.castShadow = true;
//scene.add(light);

const topLight = new THREE.DirectionalLight(0xffffff, 1); // (color, intensity)
topLight.position.set(500, 500, 500) //top-left-ish
topLight.castShadow = false;
scene.add(topLight);

const ambientLight = new THREE.AmbientLight(0x333333, 2);
scene.add(ambientLight);

// class ColorGUIHelper {
//     constructor(object, prop) {
//       this.object = object;
//       this.prop = prop;
//     }
//     get value() {
//       return `#${this.object[this.prop].getHexString()}`;
//     }
//     set value(hexString) {
//       this.object[this.prop].set(hexString);
//     }
//   }

// const gui = new GUI();
// gui.addColor(new ColorGUIHelper(light, 'color'), 'value').name('color');
// gui.add(light, 'intensity', 0, 2, 0.01);


// Tạo một camera
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 20;
camera.position.y = 1;
// camera.up.set(0, -1, 0);

let flipped = true; //or false depending any user interaction assigned
camera.up.set(0, (flipped ? -1: 0), 0);

// Tạo một renderer
var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

var mesh;

// Tạo một loader cho texture
var textureLoader = new THREE.TextureLoader();

var objLoader = new THREE.OBJLoader();
var mtlLoader = new THREE.MTLLoader();


function loadOBJ(modelDir, fileName) {
    mtlLoader.setPath(modelDir + '/');
    mtlLoader.load(fileName + '.obj.mtl', function(materials) {
        materials.preload();
        objLoader.setMaterials(materials);
        objLoader.load(modelDir + '/' + fileName + '.obj', function(object) {
            scene.add(object);
            mesh = object;
        });
    });
}


document.addEventListener('DOMContentLoaded', function() {
    var urlParams = new URLSearchParams(window.location.search);
    var fileParam = urlParams.get('file');
    var type      = urlParams.get('type');
    var modelDir  = '../models/' + fileParam;

    loadOBJ(modelDir, fileParam);
});


let controls;
controls = new THREE.OrbitControls(camera, renderer.domElement);


// Vòng lặp render
function animate() {
    requestAnimationFrame(animate);
    // Xoay vật thể liên tục
    //mesh.rotation.y += 0.01;
    renderer.render(scene, camera);
}

document.addEventListener("keydown", onDocumentKeyDown, false);
function onDocumentKeyDown(event) {
    var keyCode = event.code;
    if (keyCode == 'Space') {
        camera.up.set(0, -1, 0);
    } else if (keyCode == 'KeyQ') {
        camera.up.set(0, 0, 0);
    }
    renderer.render(scene, camera);
};

animate();
