$(document).ready(function() {
    $("#toggleTable").click(function() {
        $("#observationsTable").toggle();
        if ($("#observationsTable").is(":visible")) {
            $(this).text("Piilota havainnot");
        } else {
            $(this).text("Näytä havainnot");
        }
    });

    $("#toggleStats").click(function() {
        $("#statisticsTable").toggle();
        if ($("#statisticsTable").is(":visible")) {
            $(this).text("Piilota tilastot");
        } else {
            $(this).text("Näytä tilastot");
        }
    });
});