$(document).ready(function() {
    $("#toggleTable").click(function() {
        $("#observationsTable").toggle();
        if ($("#observationsTable").is(":visible")) {
            $(this).text("Piilota havainnot");
        } else {
            $(this).text("Näytä havainnot");
        }
    });

    $("#toggleObservationStats").click(function() {
        $("#observationStatisticsTable").toggle();
        if ($("#observationStatisticsTable").is(":visible")) {
            $(this).text("Piilota tilastot");
        } else {
            $(this).text("Näytä tilastot");
        }
    });

    $("#toggleForecastTable").click(function() {
        $("#forecastsTable").toggle();
        if ($("#forecastsTable").is(":visible")) {
            $(this).text("Piilota ennusteet");
        } else {
            $(this).text("Näytä ennusteet");
        }
    });

    $("#toggleForecastStats").click(function() {
        $("#forecastStatisticsTable").toggle();
        if ($("#forecastStatisticsTable").is(":visible")) {
            $(this).text("Piilota tilastot");
        } else {
            $(this).text("Näytä tilastot");
        }
    });

    $("#toggleAccuracyTable").click(function() {
        $("#accuracyTable").toggle();
        if ($("#accuracyTable").is(":visible")) {
            $(this).text("Piilota osuvuus");
        } else {
            $(this).text("Näytä osuvuus");
        }
    });
});