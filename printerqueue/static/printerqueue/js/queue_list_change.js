
var lst_counter =0;
$('.queue_list').forEach(function (element) {
    var picker = document.createElement("input");
    picker.type="text";
    picker.classList.add("datepicker");
    picker.name="queue_list_" + lst_counter++;

    var picker_label = document.createElement("label");
    picker_label.for=picker.name;
    picker.innerHTML="Velg Dato";


});

function loadDate(element){

}
