$(function() {
    var today = new Date();

    $("#start_date, #end_date, #quick_date").datepicker({
        dateFormat: "dd-mm-yy",
        maxDate: today,
        changeMonth: true,
        changeYear: true,
        yearRange: "c-100:c+0", // Viimeisimmät 100 vuotta
    });

    $("#start_date").datepicker({
        onSelect: function(selectedDate) {
            var startDate = $(this).datepicker("getDate");
            $("#end_date").datepicker("option", "minDate", startDate);
        }
    });

    $("#end_date").datepicker({
        onSelect: function(selectedDate) {
            var endDate = $(this).datepicker("getDate");
            $("#start_date").datepicker("option", "maxDate", endDate);
        }
    });
});