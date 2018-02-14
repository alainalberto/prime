$(document).ready( function () {
// Upper input text
   $('.upper').keyup(function() {
      $(this).val($(this).val().toUpperCase());
   });

   $('.lower').keyup(function() {
      $(this).val($(this).val().toLowerCase());
   });

// Switch
$(".switch").bootstrapSwitch();
$(".switch-min").bootstrapSwitch();


$(".btn_add_cut").click(function() {
      var column = $(this).closest('tr').children()[5].textContent;
      $('#id_customers').val(column)
      $('#customerList').modal('hide');
    });

//Data tables
   $(".data-table").DataTable();

// Messager
     $( ".messager" ).show(500, callback );
     function callback() {
      setTimeout(function() {
        $( ".messager:visible" ).removeAttr( "style" ).fadeOut();
      }, 1000 );
    };


// Script Datapicker Input
   $('.form_date').datetimepicker({
      language:  'en',
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		minView: 2,
		forceParse: 0
   });

   $('.form_time').datetimepicker({
        language:  'en',
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 1,
		minView: 0,
		maxView: 1,
		forceParse: 0
    });
   var show = false;
    $("#view").click(function() {
     if (!show){
      show = true
      $('#id_no_social').removeAttr("type", "password");
      $("#id_no_social").prop("type", "text");
      $("#view").removeClass("glyphicon glyphicon-eye-open");
      $("#view").addClass("glyphicon glyphicon-eye-close");
     }
     else{
      show = false
      $('#id_no_social').removeAttr("type", "text");
      $("#id_no_social").prop("type", "password");
      $("#view").removeClass("glyphicon glyphicon-eye-close");
      $("#view").addClass("glyphicon glyphicon-eye-open");
     }
    });


 });

function search() {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("txtsearch");
  filter = input.value.toUpperCase();
  table = document.getElementById("customer_table");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td1 = tr[i].getElementsByTagName("td")[0];
    td2 = tr[i].getElementsByTagName("td")[1];
    td3 = tr[i].getElementsByTagName("td")[2];
    td4 = tr[i].getElementsByTagName("td")[3];


      if (td1.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      }
      if (td2.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      }
      if (td3.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      }
      if (td4.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      }
       else {
        tr[i].style.display = "none";
      }

  }
}

