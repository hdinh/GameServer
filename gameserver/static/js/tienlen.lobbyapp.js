$(document).ready(function() { 
  var tables = {};

  var $tablesDataTable = $("#tables").dataTable({
    "bJQueryUI": true,
    "sPaginationType": "full_numbers",
    "aoColumns": [
      { "sClass": "name" },
      { "sClass": "dateCreated" }
    ]
  });

  function addTable(table) {
    $tablesDataTable.fnAddData([
      table.name,
      table.dateCreated
    ]);
  }

  function getSelectedRow(theTable) {
    var nodes = theTable.fnGetNodes();
    for (var i = 0; i<nodes.length; ++i) {
      if ($(nodes[i]).hasClass('row_selected')) {
        return $(nodes[i]);
      }
    }
  }

  var lobby = new TL.Lobby({
    handlers: {
      snapshot: function(snapshot) {
        var i;
        for (i=0; i < snapshot.tables.length; ++i) {
          addTable(snapshot.tables[i]);
        }
      },
      newTable: function(event) {
        addTable(event.table);
      }
    }
  });
  lobby.start();

  // Attach our handlers

  $("#tables tbody").click(function(event) {
    $($tablesDataTable.fnSettings().aoData).each(function() {
      $(this.nTr).removeClass('row_selected');
    });
    $(event.target.parentNode).addClass('row_selected');
  });
 
  $("#newGameButton").click(function() {
    TL.manager.createTable($('#tableName').val());
  });

  var existingTable, old;

  $("#joinTableButton").click(function() {
    var selected = getSelectedRow($tablesDataTable);
    if (selected) {
      var tableName = $(".name", selected).text();
      //window.open('/tables/' + tableName);
      if (!existingTable || (tableName !== old)) {
        existingTable = initTable(tableName);
        old = tableName;
      }
    }
  });
});

