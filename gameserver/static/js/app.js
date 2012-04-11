$(document).ready(function() {

    /////////////////////////////////////////
    // Constants
    /////////////////////////////////////////

    var HOST_TABLE_STRING = "Host Table";
    var JOIN_TABLE_STRING = "Join Table";

    /////////////////////////////////////////
    // Private members
    /////////////////////////////////////////

    var remote = new Remote();
    var game = new Game();
    var view = new View();

    var host_table_element = $("#host_table_input");
    var join_table_element = $("#join_table_input");

    var state = {};

    /////////////////////////////////////////
    // Private Functions
    /////////////////////////////////////////

    function on_player_handshake_complete(player) {
        state.player = player;
    }

    function on_host_table_complete(response) {
        if (response.table) {
            state.table = response.table;
        } else {
            alert(response.error);
        }
    }

    function on_join_table_complete(response) {
        if (response.table) {
            state.table = response.table;
        } else {
            alert(response.error);
        }
    }

    function on_play_now_complete(response) {
        if (response.table) {
            state.table = response.table;
        } else {
            alert(response.error);
        }
    }

    /////////////////////////////////////////
    // Main
    /////////////////////////////////////////

    $("#information_button").click(function () {
        if (host_table_element.val() != HOST_TABLE_STRING) {
            remote.host_table(host_table_element.val(), state, on_host_table_complete);
            return;
        }

        if (join_table_element.val() != JOIN_TABLE_STRING) {
            remote.join_table(join_table_element.val(), state, on_join_table_complete);
            return;
        }

        remote.play_now(state, on_play_now_complete);
    });

    host_table_element.val(HOST_TABLE_STRING);
    host_table_element.focus(function () {
        if ($(this).val() == HOST_TABLE_STRING) {
            $(this).val('').css({color:'black'});
        }
    });

    join_table_element.val(JOIN_TABLE_STRING);
    join_table_element.focus(function () {
        if ($(this).val() == JOIN_TABLE_STRING) {
            $(this).val('').css({color:'black'});
        }
    });

    view.game = game;

    remote.player_handshake(on_player_handshake_complete);
});
