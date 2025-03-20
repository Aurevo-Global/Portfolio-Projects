Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Upload an image",
        autoProcessQueue: false
    });

    dz.on("addedfile", function () {
        if (dz.files[1] != null) {
            dz.removeFile(dz.files[0]);
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;

        var url = "http://127.0.0.1:5000/classify_image";

        $.post(url, {
            image_data: imageData
        }, function (data, status) {
            console.log("Received response:", data);

            if (!data || data.length == 0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();
                $("#error").show();
                return;
            }

            let match = null;
            let bestScore = -1;
            let probabilityScores = {};

            for (let i = 0; i < data.length; ++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if (maxScoreForThisClass > bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }

            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html(`<strong>Best Match:</strong> ${match.class}`);

                let classDictionary = match.class_dictionary;
                let probabilityTable = "<table border='1'><tr><th>Class</th><th>Probability (%)</th></tr>";

                for (let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let probabilityScore = match.class_probability[index].toFixed(2); // Format to 2 decimal places
                    probabilityScores[personName] = probabilityScore;

                    probabilityTable += `<tr><td>${personName}</td><td>${probabilityScore}%</td></tr>`;
                }

                probabilityTable += "</table>";
                $("#divClassTable").html(probabilityTable);

                console.log("Probability Scores:", probabilityScores);
            }
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();
    });
}

$(document).ready(function () {
    console.log("ready!");
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});
