$(document).ready( function () {
// Upper input text
   $('.upper').keyup(function() {
      $(this).val($(this).val().toUpperCase());
   });

   $('.lower').keyup(function() {
      $(this).val($(this).val().toLowerCase());
   });
   $('#btn_new_company').click(function(){
          if (document.getElementById('new_company').checked) {

              $('#inf_company').attr("style", "display : initial;");
          }
          else {
               $('#inf_company').attr("style", "display : none;");
          }
        });

    $('#btn_ifta').click(function(){
          if (document.getElementById('ifta').checked) {

              $('#inf_ifta').attr("style", "display : initial;");
          }
          else {
            $('#inf_ifta').attr("style", "display : none;");
          }
        });

      $('#btn_dispatch').click(function(){
          if (document.getElementById('dispatch').checked) {

              $('#inf_dispatch').attr("style", "display : initial;");
          }
          else {
            $('#inf_dispatch').attr("style", "display : none;");
          }
        });

        $('#btn_apportioned').click(function(){
          if (document.getElementById('apportions').checked) {

              $('#inf_apportioned').attr("style", "display : initial;");
          }
          else {
            $('#inf_apportioned').attr("style", "display : none;");
          }
        });

        $('#btn_insurance').click(function(){
          if (document.getElementById('insurance').checked) {

              $('#inf_insurance').attr("style", "display : initial;");
          }
          else {
            $('#inf_insurance').attr("style", "display : none;");
          }
        });


// Switch
$(".switch").bootstrapSwitch();
$(".switch-min").bootstrapSwitch();


$(".btn_add_cut").click(function() {
      var column = $(this).closest('tr').children()[5].textContent;
      $('#id_customers').val(column)
      $('#customerList').modal('hide');
    });

$(".modalview").on('hidden.bs.modal', function () {
            location.reload();
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

