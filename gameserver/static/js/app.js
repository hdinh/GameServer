$(document).ready(function() {

    /////////////////////////////////////////
    // Private members
    /////////////////////////////////////////

    var remote = new Remote();
    var game = new Game();
    var view = new View();
    var JOIN_TABLE_STRING = "Join Table";
    var state = {};

    /////////////////////////////////////////
    // Private Functions
    /////////////////////////////////////////

    function on_player_handshake_complete(player) {
        state.player = player;
        $("#self").text("Play now");
        $("#opponent").val(JOIN_TABLE_STRING).css({color:'grey'});
    }

    function on_join_game_complete(game) {
        view.current_stage = view.StageEnum.CONTINUE_PROMPT;
        alert("GAMING");
    }

    /////////////////////////////////////////
    // Main
    /////////////////////////////////////////

    $("#information_button").click(function () {
        view.current_stage = view.StageEnum.EXCHANGE_PROMPT;
        remote.player_handshake(on_player_handshake_complete);
    });

    $("#exchange_button").click(function () {
        if ($("#opponent").val() == JOIN_TABLE_STRING) {
            remote.join_game(state.player, on_join_game_complete);
        } else {
            view.current_stage = view.StageEnum.WAIT_PROMPT;
            alert("TODO");
        }
    });

    $("#opponent").focus(function () {
        if ($(this).val() == JOIN_TABLE_STRING) {
            $(this).val('').css({color:'black'});
        }
    });

    view.game = game;
});
