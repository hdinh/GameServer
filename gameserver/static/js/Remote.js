function Remote() {
    var self = this;

    self.player_handshake = function (callback) {
        $.ajax({
            type: "POST",
            url: "/api/player/handshake",
            success: function (data) {
                callback(JSON.parse(data));
            }
        });
    };

    self.join_game = function (player, callback) {
        $.ajax({
            type: "POST",
            url: "/api/games/join",
            data: player,
            success: function (data) {
                callback(JSON.parse(data));
            }
        });
    };
}
