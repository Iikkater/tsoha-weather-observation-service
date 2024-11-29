$(document).ready(function() {
    $("#toggleTable").click(function() {
        $("#observationsTable").toggle();
        if ($("#observationsTable").is(":visible")) {
            $(this).text("Piilota havainnot");
        } else {
            $(this).text("Näytä havainnot");
        }
    });
});