$(function() {
    var today = new Date();

    $("#start_date").datepicker({
        dateFormat: "dd-mm-yy",
        maxDate: today,
        changeMonth: true,
        changeYear: true,
        yearRange: "c-100:c+0", // Viimeiimmät 100 vuotta
        onSelect: function(selectedDate) {
            var startDate = $(this).datepicker("getDate");
            $("#end_date").datepicker("option", "minDate", startDate);
        }
    });

    $("#end_date").datepicker({
        dateFormat: "dd-mm-yy",
        maxDate: today,
        changeMonth: true,
        changeYear: true,
        yearRange: "c-100:c+0", // Viimeisimmät 100 vuotta
        onSelect: function(selectedDate) {
            var endDate = $(this).datepicker("getDate");
            $("#start_date").datepicker("option", "maxDate", endDate);
        }
    });
});