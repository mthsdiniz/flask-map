const map = L.map('map').setView([0, 0], 2); // Set your desired initial location and zoom level

const apiKey = "AAPK238c225846434baf9062c66e568f5b43ny9IAYM60GGzeNQCgyyn9vfA_74BNEj_1oV6-WceJ7r_IlvVWWE1t-2SVsqygApe";

L.esri.Vector.vectorBasemapLayer("ArcGIS:Imagery", {
  apikey: apiKey
}).addTo(map);

//L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

function fetchFiles() {
    const owner = $('#owner-input').val();
    const repo = $('#repo-input').val();
    const gh_token = $('#gh-token').val();
    $.getJSON(`/get-files?owner=${owner}&repo=${repo}&ghtoken=${gh_token}`, function (files) {
        const select = $('#file-select');

        for (const file of files) {
            if (file.name.endsWith('.geojson') || file.name.endsWith('.kml')) {
                select.append($('<option>', {
                    value: file.url,
                    text: file.name
                }));
            }
        }
    });
}

// Call the fetchFiles function when the page loads
$('#load-btn').on('click',function(){
    fetchFiles();
});

let layer;

$("#file-select").change(function () {
    const selectedFile = $(this).val();
    const file_type = selectedFile.split('.').pop().split('?').shift();
    const gh_token = $('#gh-token').val();
    
    console.log(file_type)

    if (file_type === "geojson") {
        fetch(`/fetch-file?url=${selectedFile}&ghtoken=${gh_token}`)
            .then(response => response.json())
            .then(data => {
                if (layer) {
                    map.removeLayer(layer);
                }
                layer = L.geoJSON(data).addTo(map);
                map.fitBounds(layer.getBounds());

            });
    } else if (file_type === "kml") {
        fetch(`/fetch-file?url=${selectedFile}&ghtoken=${gh_token}`)
            .then(response => response.text())
            .then(data => {
                if (layer) {
                    map.removeLayer(layer);
                }

                const format = (selectedFile.endsWith('.geojson') ? 'geojson' : 'kml');
                layer = omnivore[format].parse(data).addTo(map);
                map.fitBounds(layer.getBounds());
            });
    }
});

// Enable search functionality
$('#search').on('keyup', function () {
    const value = $(this).val().toLowerCase();

    $('#file-select option').filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
});