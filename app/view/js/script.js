document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    const uploadButton = event.target.querySelector('button[type="submit"]');
    uploadButton.disabled = true;
    uploadButton.textContent = 'Carregando...';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('message').textContent = data.error;
        } else {
            document.getElementById('message').textContent = data.message;
            document.getElementById('downloadLink').href = data.download_url;
            document.getElementById('downloadLink').style.display = 'block';
        }
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Erro ao enviar o arquivo';
    })
    .finally(() => {
        uploadButton.disabled = false;
        uploadButton.textContent = 'Upload';
    });
});

document.getElementById('filterForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const filters = {
        VeiculoEquip: document.getElementById('veiculoEquip').value,
        DataInicial: document.getElementById('dataInicial').value,
        DataFinal: document.getElementById('dataFinal').value
    };
    
    const filterButton = event.target.querySelector('button[type="submit"]');
    filterButton.disabled = true;
    filterButton.textContent = 'Filtrando...';

    fetch('/filter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filters)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('message').textContent = data.error;
        } else {
            document.getElementById('message').textContent = data.message;
            document.getElementById('downloadFilteredLink').href = data.download_url;
            document.getElementById('downloadFilteredLink').style.display = 'block';
        }
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Erro ao aplicar os filtros';
    })
    .finally(() => {
        filterButton.disabled = false;
        filterButton.textContent = 'Aplicar Filtros';
    });
});

document.getElementById('cleanAndExit').addEventListener('click', function() {
    const cleanButton = document.getElementById('cleanAndExit');
    cleanButton.disabled = true;
    cleanButton.textContent = 'Limpando e Fechando...';

    fetch('/clean_and_exit', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').textContent = data.message;
        window.setTimeout(() => {
            window.close(); //Close window do nav
        }, 2000);
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Sucesso em limpar os arquivos e finalizar o servidor';
    })
    .finally(() => {
        cleanButton.disabled = false;
        cleanButton.textContent = 'Limpar e Fechar';
    });
});