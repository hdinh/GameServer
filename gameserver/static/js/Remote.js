function Remote() {

    this.player_handshake = function (callback) {
        $.ajax({
            type: "POST",
            url: "/api/player/handshake",
            success: function (data) {
                callback(JSON.parse(data));
            }
        });
    };

    this.host_table = function (table_name, state, callback) {
        $.ajax({
            type: "POST",
            url: "/api/games",
            data: {
                "method" : "host",
                "state" : JSON.stringify(state),
                "table_name" : table_name
            },
            success: function (data) {
                callback(JSON.parse(data));
            }
        });
    };

    this.join_table = function (table_name, state, callback) {
        $.ajax({
            type: "POST",
            url: "/api/games",
            data: {
                "method" : "join",
                "state" : JSON.stringify(state),
                "table_name" : table_name
            },
            success: function (data) {
                callback(JSON.parse(data));
            }
        });
    };

    this.play_now = function (state, callback) {
        $.ajax({
            type: "POST",
            url: "/api/games",
            data: {
                "method" : "play_now",
                "state" : JSON.stringify(state)
            },
            success: function (data) {
                callback(JSON.parse(data));
            }
        });
    };
}
