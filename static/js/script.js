const imageInput = document.getElementById('image-input');
const uploadArea = document.getElementById('upload-area');
const uploadPlaceholder = document.getElementById('upload-placeholder');
const previewImg = document.getElementById('preview-img');
const loadingState = document.getElementById('loading-state');
const resultsCard = document.getElementById('results-card');

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.background = '#F1F8E9';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.background = '';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.background = '';
    if (e.dataTransfer.files.length) {
        handleImage(e.dataTransfer.files[0]);
    }
});

imageInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleImage(e.target.files[0]);
    }
});

function handleImage(file) {
    const reader = new FileReader();
    reader.onload = () => {
        previewImg.src = reader.result;
        previewImg.style.display = 'block';
        uploadPlaceholder.style.display = 'none';
        detectDisease(file);
    };
    reader.readAsDataURL(file);
}

async function detectDisease(imageFile) {
    loadingState.style.display = 'block';
    resultsCard.style.display = 'none';

    const formData = new FormData();
    formData.append('file', imageFile);

    try {
        const res = await fetch('/', { method: 'POST', body: formData });
        const data = await res.json();

        loadingState.style.display = 'none';
        resultsCard.style.display = 'block';

        document.getElementById('disease-title').textContent = data.disease;
        document.getElementById('severity-text').textContent = data.severity;
        document.getElementById('disease-cause').textContent = data.cause;
        document.getElementById('organic-cure').textContent = data.organic_cure;
        document.getElementById('chemical-cure').textContent = data.chemical_cure;
        document.getElementById('prevention').textContent = data.prevention;
        document.getElementById('health-score').textContent = data.health_score + '/100';

        const meterFill = document.getElementById('meter-fill');
        if (data.severity === 'High') meterFill.style.width = '90%';
        else if (data.severity === 'Medium') meterFill.style.width = '65%';
        else if (data.severity === 'Low') meterFill.style.width = '30%';
        else meterFill.style.width = '10%';

        if (data.has_heatmap) {
            document.getElementById('heatmap-container').style.display = 'block';
            document.getElementById('heatmap-img').src = '/static/heatmap.jpg?t=' + new Date().getTime();
        } else {
            document.getElementById('heatmap-container').style.display = 'none';
        }

        resultsCard.scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        loadingState.style.display = 'none';
        alert('Error: ' + err.message);
    }
}

function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}